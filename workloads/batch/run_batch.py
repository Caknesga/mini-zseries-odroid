import time
while True:
    with open("/tmp/batch_log.txt", "a") as f:
        f.write(f"Batch job executed at {time.ctime()}\n")
    time.sleep(30)
    