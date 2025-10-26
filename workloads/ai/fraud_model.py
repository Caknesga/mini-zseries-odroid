import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd, joblib
from sklearn.preprocessing import LabelEncoder


np.random.seed(42)
n = 2000

data = []

for _ in range(n):
    amount = np.random.randint(1, 20000)
    fraud = 1 if amount > 5000 else 0
    # Add some randomness       
    if np.random.rand() < 0.05: 
        fraud = 1 - fraud

        data.append([amount, fraud])

df = pd.DataFrame(data, columns=[ "amount", "fraud"])


X = df[["amount"]]
y = df["fraud"]

# Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)
preds = model.predict(X_test)

print(classification_report(y_test, preds, digits=3))

joblib.dump(model, "fraud_model.pkl")
print("✅ Simple fraud model saved as fraud_model.pkl")
