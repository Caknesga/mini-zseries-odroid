import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd, joblib
from sklearn.preprocessing import LabelEncoder

model = joblib.load("fraud_model.pkl")
np.random.seed(42)
n = 1000

account_types = ["student", "worker", "business"]
data = []

for acc in account_types:
    for _ in range(n):
        amount = np.random.randint(1, 20000)
        intl = np.random.randint(0, 2)
        night = np.random.randint(0, 2)
        
        # Fraud logic per profile
        if acc == "student":
            fraud = 1 if amount > 500 else 0
        elif acc == "worker":
            fraud = 1 if amount > 1000 else 0
        elif acc == "business":
            fraud = 1 if amount > 30000 else 0

        # Add some randomness (5% noise)
        if np.random.rand() < 0.05:
            fraud = 1 - fraud

        data.append([acc, amount, intl, night, fraud])

df = pd.DataFrame(data, columns=["account_type", "amount", "international", "night", "fraud"])

le = LabelEncoder()
df["account_type"] = le.fit_transform(df["account_type"])  # student=2, ceo=0, etc.

X_new = df[["account_type", "amount", "international", "night"]]
y_new= df["fraud"]

model.fit(X_new, y_new)

joblib.dump(model, "fraud_model.pkl")
