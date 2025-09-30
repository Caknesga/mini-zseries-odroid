from flask import Flask, request, jsonify
import joblib
import numpy as np
import threading
import os

app = Flask(__name__)
accounts = {"A": 1000, "B": 2000, "C": 1500}
lock = threading.Lock()

# Pfad zum Modell (nach scp)
MODEL_PATH = "workloads/fraud_model.pkl"


# Lade Modell + optionalen Scaler
model = joblib.load(MODEL_PATH)
scaler = None

def feature_vector_from_payload(payload):
    # Beispielfeatures: [amount, is_international, is_night]
    amount = float(payload.get("amount", 0))
    intl = int(payload.get("is_international", 0))
    night = int(payload.get("is_night", 0))
    x = np.array([[amount, intl, night]])
    if scaler is not None:
        x = scaler.transform(x)
    return x

@app.route("/transaction", methods=["POST"])
def transaction():
    data = request.json or {}
    account = data.get("account")
    if account not in accounts:
        return jsonify({"error": "Account not found"}), 404

    x = feature_vector_from_payload(data)
    pred = model.predict(x)[0]            # 1 = fraud, 0 = normal
    prob = None
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(x)[0, 1])

    if pred == 1:
        # optional: log, block, raise alert
        return jsonify({"status": "rejected", "reason": "fraud suspected", "score": prob}), 403

    # Beispiel: deposit oder withdraw (hier deposit)
    with lock:
        accounts[account] += float(data.get("amount", 0))
    return jsonify({"status": "approved", "account": account, "balance": accounts[account], "score": prob})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
