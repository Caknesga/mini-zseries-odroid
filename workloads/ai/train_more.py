import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

# Load historical data
df = pd.read_json("transactions.json")  # or however you store it

# Extract features
X_new = df[["amount"]]                # features
y_new = df["fraud_label"]             # target

# Load old model
model = joblib.load("fraud_model.pkl")

# Retrain / fine-tune
model.fit(X_new, y_new)

# Save updated model
joblib.dump(model, "fraud_model.pkl")
print("✅ Fraud model retrained with new data.")
