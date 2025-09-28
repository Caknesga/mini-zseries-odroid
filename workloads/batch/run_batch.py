import time

while True:
    message = f"Batch job executed at {time.ctime()}"
    print(message)
    with open("/tmp/batch_log.txt", "a") as f:
        f.write(message + "\n")   # Nur eine Zeile pro Loop
    time.sleep(5)
    