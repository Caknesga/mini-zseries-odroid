import requests
import random
import threading

ODROID_IP = "192.168.1.9" #anpassen für lokale Netzwerk
PORT = 5050
URL = f"http://{ODROID_IP}:{PORT}"

accounts = ["A", "B", "C"]

def random_transaction():
    account = random.choice(accounts)
    action = random.choice(["deposit", "withdraw"])
    amount = random.randint(1, 50)

    if action == "deposit":
        r = requests.post(f"{URL}/deposit", json={"account": account, "amount": amount})
    else:
        r = requests.post(f"{URL}/withdraw", json={"account": account, "amount": amount})

    print(f"{action} {amount} on {account} → {r.json()}")

# 100 Threads
threads = []
for _ in range(100):
    t = threading.Thread(target=random_transaction)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Endstand prüfen
for acc in accounts:
    balance = requests.get(f"{URL}/balance/{acc}").json()
    print(f"Final {acc}: {balance}")
