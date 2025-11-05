import requests
import random
import threading

ODROID_IP = "192.168.178.114" #anpassen für lokale Netzwerks
PORT = 5050
URL = f"http://{ODROID_IP}:{PORT}"  # or your Flask API address
accounts = ["Deniz", "Markus", "IBM"]

def run_random_transactions(n=10):
    count = 0
    for _ in range(n):
        account = random.choice(accounts)
        action = random.choice(["deposit", "withdraw"])
        amount = random.randint(1, 500)

        try:
            r = requests.post(f"{URL}/{action}", json={"account": account, "amount": amount})
            if r.status_code == 200:
                count += 1
        except Exception as e:
            print("Transaction failed:", e)
    return count