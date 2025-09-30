import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Mehr Datenpunkte generieren
np.random.seed(42)
X = np.random.randint(0, 1000, size=(200, 3))  # 200 Transaktionen
y = ((X[:,0] > 500) & (X[:,1] == 1) | (X[:,2] == 1)).astype(int)  # Regel: Fraud wenn Betrag hoch & international oder nachts

# Splitten
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

model = LogisticRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)

print(classification_report(y_test, preds))
joblib.dump(model, "fraud_model.pkl")

