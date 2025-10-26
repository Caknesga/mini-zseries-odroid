from flask import Flask, request, jsonify, render_template
import threading
import json, os
from datetime import datetime
import psutil
import time
import platform 
import joblib
import numpy as np


app = Flask(__name__)
accounts = {"Deniz": 1000, "Markus": 3000, "IBM": 1500000}
lock = threading.Lock()  # Für Konsistenz
transactions = []  # or load from 'transactions.json' if you want persistence
account_stats = {} # to track stats per account for fraud detection
fraud_model = joblib.load("fraud_model.pkl")

def save_state():
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_state():
    global accounts
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
    else:
        accounts = {"Deniz": 1000, "Markus": 2000, "IBM": 1500}

def log_transaction(tx_type, account=None, from_acc=None, to_acc=None, amount=0, status="success"):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": tx_type,
        "account": account,
        "from": from_acc,
        "to": to_acc,
        "amount": amount,
        "status": status,
       
    }
    transactions.append(entry)

def update_account_stats(account, amount): # track stats for fraud detection 
    if account not in account_stats:
        account_stats[account] = {"count": 0, "total": 0, "mean": 0}
    stats = account_stats[account]
    stats["count"] += 1
    stats["total"] += amount
    stats["mean"] = stats["total"] / stats["count"]

def predict_fraud(account, amount): 
    """Combine global model with local account behavior."""
    if fraud_model is None:
        return 0.0

    # Global model baseline probability
    base_prob = fraud_model.predict_proba(np.array([[amount]]))[0][1]

    # Local account behavior adjustment
    if account in account_stats and account_stats[account]["count"] > 5:
        mean_amt = account_stats[account]["mean"]
        deviation = abs(amount - mean_amt) / (mean_amt + 1)
        adjusted_prob = min(1.0, base_prob + deviation * 0.3)
    else:
        adjusted_prob = base_prob

    return round(adjusted_prob, 3)

@app.route("/")
def index():
    # Beispiel in Flask
    thresholds = {"Deniz": 100, "Markus": 500, "IBM": 100000}
    return render_template("index.html", accounts=accounts, thresholds=thresholds)

        
@app.route("/balance/<account>", methods=["GET"])
def get_balance(account):
    if account not in accounts:
        save_state()
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account": account, "balance": accounts[account]})

@app.route("/deposit", methods=["POST"])
def deposit():
    account = request.json.get("account")
    amount = request.json.get("amount", 0)
    if account not in accounts:
        log_transaction("deposit", account=account, amount=amount, status="failed")
        return jsonify({"error": "Account not found"}), 404
    with lock:
        accounts[account] += amount
        save_state()          # <-- FIX
        log_transaction("deposit", account=account, amount=amount)
        update_account_stats(account, amount)

        return jsonify({"account": account, "balance": accounts[account]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    account = request.json.get("account")
    amount = request.json.get("amount", 0)
    if account not in accounts:
        log_transaction("withdraw", account=account, amount=amount, status="failed")

        return jsonify({"error": "Account not found"}), 404
    with lock:
        if accounts[account] >= amount:
            accounts[account] -= amount
            save_state()
            log_transaction("withdraw", account=account, amount=amount)
            update_account_stats(account, amount)
            return jsonify({"account": account, "balance": accounts[account]})
        else:
            save_state()
            log_transaction("withdraw", account=account, amount=amount, status="failed")

            return jsonify({"error": "Not enough funds"}), 400

@app.route("/transfer", methods=["POST"])
def transfer():
    from_account = request.json.get("from")
    to_account = request.json.get("to")
    amount = request.json.get("amount", 0)

    if from_account not in accounts or to_account not in accounts:
        log_transaction("transfer", account=to_account, from_acc=from_account, to_acc=to_account, amount=amount, status="failed")

        return jsonify({"error": "One or both accounts not found"}), 404

    if from_account == to_account:
        return jsonify({"error": "Source and destination must be different"}), 400

    with lock:
        if accounts[from_account] >= amount:
            accounts[from_account] -= amount
            accounts[to_account] += amount
            save_state()
            log_transaction("transfer", from_acc=from_account, to_acc=to_account, amount=amount)
            update_account_stats(from_account, amount)
            update_account_stats(to_account, amount)
            return jsonify({
                "from": from_account,
                "to": to_account,
                "amount": amount,
                "balances": accounts
            })
        else:
            log_transaction("transfer", from_acc=from_account, to_acc=to_account, amount=amount, status="failed")

            return jsonify({"error": "Not enough funds"}), 400
        
@app.route("/transactions", methods=["GET"])
def latest_transaction():
   return jsonify(transactions)

@app.route("/account_stats")
def get_stats():
    return jsonify(account_stats)

@app.route("/hardware")
def hardware_status():

    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    per_core_cpu= psutil.cpu_percent(percpu=True)
    per_core_freq = [f._asdict() for f in psutil.cpu_freq(percpu=True)]     
    io_stats = psutil.disk_io_counters()._asdict()
    
    # Fallback temperature for ARM (Odroid, RPi)
    temperature = None
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temperature = int(f.read()) / 1000.0
    except FileNotFoundError:
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for _, entries in temps.items():
                    if entries:
                        temperature = entries[0].current
                        break
        except Exception:
            pass

    return jsonify({
        "cpu_percent": cpu_percent,
        "per_core_cpu": per_core_cpu,
        "cpu_freq": cpu_freq._asdict() if cpu_freq else {},
        "cpu_freq_per_core": per_core_freq,
        "memory_percent": mem.percent,
        "disk_percent": disk.percent,
        "disk_io": io_stats,
        "network": {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        },
        "load_avg": os.getloadavg(),
        "temperature": temperature if temperature else "Not supported",
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "platform": platform.platform()
    })



if __name__ == "__main__":
    load_state()
    app.run(host="0.0.0.0", port=5050)
    try:
        fraud_model = joblib.load("fraud_model.pkl")
        print("✅ Fraud model loaded successfully.")
    except:
        fraud_model = None
        print("⚠️ Warning: Fraud model not found.")
