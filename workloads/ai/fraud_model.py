import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

#  Transaktionen generieren
np.random.seed(42)
n = 1000
amounts = np.random.randint(1, 2000, n)          
international = np.random.randint(0, 2, n)       
night = np.random.randint(0, 2, n)               

X = np.column_stack([amounts, international, night])

# Labels
y = []
for a, intl, nt in X:
    if a > 1000 and intl == 1:     
        label = 1
    elif nt == 1 and a > 200:   
        label = 1
    else:
        label = 0
    
    # Zufällig 5% der Labels umdrehen (Noise)
    if np.random.rand() < 0.05:
        label = 1 - label
    y.append(label)

y = np.array(y)

# Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)
preds = model.predict(X_test)

print(classification_report(y_test, preds, digits=3))

joblib.dump(model, "fraud_model.pkl")


