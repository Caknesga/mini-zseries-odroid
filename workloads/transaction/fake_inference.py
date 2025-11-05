import math, time, random

def simulate_inference(intensity=300000):
    """Simulate CPU load like AI inference (no real AI)."""
    print(f"[Fake AI] Simulating inference with intensity={intensity}")
    while True:
        # compute-heavy loop
        x = 0.0
        for i in range(intensity):
            x += math.sin(i) * math.cos(i)
        # short sleep to make CPU usage more realistic
        time.sleep(0.05 + random.random() * 0.02)

if __name__ == "__main__":
    simulate_inference()