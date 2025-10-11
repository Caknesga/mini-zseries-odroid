import requests
import random
import threading

ODROID_IP = "192.168.1.9" #anpassen für lokale Netzwerks
PORT = 5050
URL = f"http://{ODROID_IP}:{PORT}"

accounts = ["A", "B", "C"]

def random_transaction():
    account = random.choice(accounts)
    action = random.choice(["deposit", "withdraw"])
    amount = random.randint(1, 1000)

    if action == "deposit":
            r = requests.post(f"{URL}/deposit", json={"account": account, "amount": amount})
            print(f"Deposit {amount} → {account}: {r.json()}")

    elif action == "withdraw":
        r = requests.post(f"{URL}/withdraw", json={"account": account, "amount": amount})
        print(f"Withdraw {amount} ← {account}: {r.json()}")

    elif action == "transfer":
        from_acc = random.choice(accounts)
        to_acc = random.choice([a for a in accounts if a != from_acc])
        r = requests.post(f"{URL}/transfer", json={"from": from_acc, "to": to_acc, "amount": amount})
        print(f"Transfer {amount} from {from_acc} to {to_acc}: {r.json()}")

# 10 Threads
threads = []
for _ in range(10):
    t = threading.Thread(target=random_transaction)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Endstand prüfen
for acc in accounts:
    balance = requests.get(f"{URL}/balance/{acc}").json()
    print(f"Final {acc}: {balance}")
