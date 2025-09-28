from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
balance = 1000  # Startguthaben
lock = threading.Lock()  # Für Konsistenz

@app.route("/balance", methods=["GET"])
def get_balance():
    return jsonify({"balance": balance})

@app.route("/deposit", methods=["POST"])
def deposit():
    global balance
    amount = request.json.get("amount", 0)
    with lock:
        balance += amount
    return jsonify({"balance": balance})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    global balance
    amount = request.json.get("amount", 0)
    with lock:
        if balance >= amount:
            balance -= amount
            return jsonify({"balance": balance})
        else:
            return jsonify({"error": "Not enough funds"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
