import math, time, random, argparse, multiprocessing, os

def simulate_inference(intensity=500_000, workers=2):
    """Simulate parallel AI inference load (multi-core)."""
    print(f"[Fake AI] Starting {workers} workers with intensity={intensity}")
    def heavy_loop(intensity):
        while True:
            acc = 0.0
            for i in range(intensity):
                acc += math.sin(i) * math.cos(i)
            # only a tiny pause so it doesn’t lock the board
            time.sleep(0.01 + random.random() * 0.005)

    # Launch N worker processes
    procs = []
    for _ in range(workers):
        p = multiprocessing.Process(target=heavy_loop, args=(intensity,))
        p.daemon = True
        p.start()
        procs.append(p)

    print(f"[Fake AI] PID={os.getpid()} running")
    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--intensity", type=int, default=500_000)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    simulate_inference(args.intensity, args.workers)
