import json, os, numpy as np

PARAMS_PATH = os.path.join(os.path.dirname(__file__), "lr_params.json")
with open(PARAMS_PATH, "r") as f:
    P = json.load(f)

COEF = np.array(P["coef"])                # (1, n)
INTERCEPT = np.array(P["intercept"]).reshape(-1)  # (1,)
SCALER = P.get("scaler")

def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))

def _prep(x: np.ndarray) -> np.ndarray:
    # x shape: (n_features,)
    if SCALER:
        mean = np.array(SCALER["mean"])
        scale = np.array(SCALER["scale"])
        x = (x - mean) / scale
    return x

def predict_proba_amount(amount: float) -> float:
    # your model uses only "amount" → vector of length 1
    x = np.array([float(amount)], dtype=float)
    x = _prep(x)
    logit = float(COEF @ x + INTERCEPT)   # (1,n)·(n,) + (1,) → scalar
    return _sigmoid(logit)

def predict_amount(amount: float, thresh: float = 0.5) -> int:
    return 1 if predict_proba_amount(amount) >= thresh else 0