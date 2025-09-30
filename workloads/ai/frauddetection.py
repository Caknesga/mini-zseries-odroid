# workloads/fraud/fraud_detection.py
import json
import random
import time
from sklearn.ensemble import IsolationForest
import numpy as np

# Beispiel: normale Transaktionen (kleine Beträge)
normal_data = np.array([[random.randint(1, 200)] for _ in range(200)])
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(normal_data)

transactions = []

# Simuliere neue Transaktionen
for i in range(50):
    amount = random.choice([random.randint(1, 200), random.randint(1000, 5000)])  # manchmal verdächtig hoch
    transactions.append({"account": random.choice(["A", "B", "C"]),
                         "amount": amount,
                         "type": random.choice(["deposit", "withdraw"]),
                         "timestamp": time.time()})

# Feature-Vektor: nur Betrag
X_test = np.array([[t["amount"]] for t in transactions])
preds = model.predict(X_test)

with open("/tmp/fraud_log.txt", "w") as f:
    for t, p in zip(transactions, preds):
        if p == -1:  # -1 = Anomalie
            f.write(f"FRAUD SUSPECT: {json.dumps(t)}\n")
        else:
            f.write(f"OK: {json.dumps(t)}\n")

print("Fraud detection batch finished. Check /tmp/fraud_log.txt")
