import requests
import random
import threading

ODROID_IP = "192.168.178.114" #anpassen für lokale Netzwerks
PORT = 5050
URL = f"http://{ODROID_IP}:{PORT}"

accounts = ["A", "B", "C"]

def random_transaction():
    account = random.choice(accounts)
    action = random.choice(["deposit", "withdraw","transfer"])
    amount = random.randint(1, 1000)

    if action == "deposit":
            r = requests.post(f"{URL}/deposit", json={"account": account, "amount": amount})
            print(f"Deposit {amount} → {account}: {r.json()}")

    elif action == "withdraw":
        r = requests.post(f"{URL}/withdraw", json={"account": account, "amount": amount})
        print(f"Withdraw {amount} ← {account}: {r.json()}")

    elif action == "transfer":
        
        to_acc = random.choice([a for a in accounts if a != account])
        r = requests.post(f"{URL}/transfer", json={"from": account, "to": to_acc, "amount": amount})
        print(f"Transfer {amount} from {account} to {to_acc}: {r.json()}")

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
