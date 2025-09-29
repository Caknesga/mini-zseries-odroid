import requests
import random
import threading

ODROID_IP = "192.168.1.9"   # anpassen falls nötig
PORT = 5050
URL = f"http://{ODROID_IP}:{PORT}"

def random_transaction():
    action = random.choice(["deposit", "withdraw"])
    amount = random.randint(1, 50)

    if action == "deposit":
        r = requests.post(f"{URL}/deposit", json={"amount": amount})
    else:
        r = requests.post(f"{URL}/withdraw", json={"amount": amount})

    print(f"{action} {amount} → {r.json()}")

# 50 Threads starten
threads = []
for _ in range(50):
    t = threading.Thread(target=random_transaction)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Endstand prüfen
final_balance = requests.get(f"{URL}/balance").json()
print("Final balance:", final_balance)
