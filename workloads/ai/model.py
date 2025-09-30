import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Dummy-Daten: [amount, is_international, is_night_time]
X = np.array([
    [20, 0, 0], [500, 1, 1], [5, 0, 0], [1000, 1, 0],
    [50, 0, 1], [200, 1, 1], [15, 0, 0], [300, 0, 1]
])
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])  # 0 = normal, 1 = fraud

# Split + Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LogisticRegression()
model.fit(X_train, y_train)

# Test Accuracy
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

# Speichern
joblib.dump(model, "fraud_model.pkl")
print("Model saved as fraud_model.pkl")
