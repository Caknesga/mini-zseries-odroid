from flask import Flask, request, jsonify, render_template
import threading
import json, os
from datetime import datetime


app = Flask(__name__)
accounts = {"A": 1000, "B": 3000, "C": 1500000}
lock = threading.Lock()  # Für Konsistenz
transactions = []  # or load from 'transactions.json' if you want persistence

def save_state():
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_state():
    global accounts
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
    else:
        accounts = {"A": 1000, "B": 2000, "C": 1500}

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


@app.route("/")
def index():
    # Beispiel in Flask
    thresholds = {"A": 100, "B": 500, "C": 100000}
    return render_template("index.html", accounts=accounts, thresholds=thresholds)

        
@app.route("/balance/<account>", methods=["GET"])
def get_balance(account):
    if account not in accounts:
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
def get_transactions():
    return jsonify(transactions)

if __name__ == "__main__":
    load_state()
    app.run(host="0.0.0.0", port=5050)
