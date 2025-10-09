from flask import Flask, request, jsonify, render_template
import threading
import json, os


app = Flask(__name__)
accounts = {"A": 1000, "B": 2000, "C": 1500}
lock = threading.Lock()  # Für Konsistenz

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


@app.route("/")
def index():
    return render_template("index.html", accounts=accounts)

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
        return jsonify({"error": "Account not found"}), 404
    with lock:
        accounts[account] += amount
        save_state()          # <-- FIX
    return jsonify({"account": account, "balance": accounts[account]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    account = request.json.get("account")
    amount = request.json.get("amount", 0)
    if account not in accounts:
        return jsonify({"error": "Account not found"}), 404
    with lock:
        if accounts[account] >= amount:
            accounts[account] -= amount
            save_state()
            return jsonify({"account": account, "balance": accounts[account]})
        else:
            save_state()
            return jsonify({"error": "Not enough funds"}), 400

if __name__ == "__main__":
    load_state()
    app.run(host="0.0.0.0", port=5050)
