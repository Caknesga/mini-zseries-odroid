from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
accounts = {"A": 1000, "B": 2000, "C": 1500}
lock = threading.Lock()  # Für Konsistenz

@app.route("/balance", methods=["GET"])
def get_balance(account):
    if account not in accounts:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account": account, "balance": accounts[account]})

@app.route("/deposit", methods=["POST"])
def deposit():
    global accounts
    account = request.json.get("account")
    amount = request.json.get("amount", 0)
    if account not in accounts:
        return jsonify({"error": "Account not found"}), 404
    with lock:
        balance += amount
    return jsonify({"account": account, "balance": accounts[account]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    global accounts
    account = request.json.get("account")
    amount = request.json.get("amount", 0)
    if account not in accounts:
        return jsonify({"error": "Account not found"}), 404
    with lock:
        if accounts[account] >= amount:
            accounts[account] -= amount
            return jsonify({"account": account, "balance": accounts[account]})
        else:
            return jsonify({"error": "Not enough funds"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
