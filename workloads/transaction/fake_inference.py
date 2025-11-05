import math, time, random, argparse, multiprocessing, os, signal

STOP_FILE = "/tmp/fake_ai_stop.flag"

def heavy_loop(intensity):
    while True:
        # check for stop signal
        if os.path.exists(STOP_FILE):
            break
        acc = 0.0
        for i in range(intensity):
            acc += math.sin(i) * math.cos(i)
        time.sleep(0.01 + random.random() * 0.005)

def simulate_inference(intensity=500_000, workers=2):
    # remove old stop file
    if os.path.exists(STOP_FILE):
        os.remove(STOP_FILE)

    print(f"[Fake AI] Starting {workers} workers (intensity={intensity})")

    procs = []
    for _ in range(workers):
        p = multiprocessing.Process(target=heavy_loop, args=(intensity,))
        p.daemon = True
        p.start()
        procs.append(p)

    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        pass
    finally:
        print("[Fake AI] Inference stopped gracefully.")
        for p in procs:
            if p.is_alive():
                p.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--intensity", type=int, default=500_000)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    simulate_inference(args.intensity, args.workers)
