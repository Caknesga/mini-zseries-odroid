import joblib, json, numpy as np

model = joblib.load("fraud_model.pkl")      # your trained LogisticRegression

# if you also saved a StandardScaler, export it too (optional)
scaler = None
try:
    scaler = joblib.load("scaler.pkl")
except:
    pass

params = {
    "coef": model.coef_.tolist(),           # shape (1, n_features)
    "intercept": model.intercept_.tolist(), # shape (1,)
    "scaler": None
}

if scaler is not None:
    params["scaler"] = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist()
    }

with open("lr_params.json", "w") as f:
    json.dump(params, f)

print("Exported lr_params.json")