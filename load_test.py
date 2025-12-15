import asyncio
import httpx
import time
import csv
import matplotlib.pyplot as plt

URL = "http://localhost:8000/facts/random"
CONCURRENT_REQUESTS = 50
TOTAL_REQUESTS = 500
OUTPUT_CSV = "latency_report.csv"
LATENCY_PLOT = "latency_plot.png"

latencies = []

async def fetch(client, index):
    """Send a single GET request and record latency."""
    start = time.perf_counter()
    status = "ERROR"
    try:
        response = await client.get(URL)
        status = response.status_code
    except Exception as e:
        status = f"ERROR: {e}"
    end = time.perf_counter()

    latencies.append({
        "request": index,
        "latency_ms": (end - start) * 1000,
        "status": status
    })

async def run_batch(client, start_index, end_index):
    """Run a batch of requests concurrently."""
    tasks = [fetch(client, i) for i in range(start_index, end_index)]
    await asyncio.gather(*tasks)

async def main():
    async with httpx.AsyncClient(timeout=20.0) as client:
        for i in range(0, TOTAL_REQUESTS, CONCURRENT_REQUESTS):
            batch_end = min(i + CONCURRENT_REQUESTS, TOTAL_REQUESTS)
            await run_batch(client, i, batch_end)
            print(f"Completed requests {i+1}-{batch_end}")

    # Save CSV
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["request", "latency_ms", "status"])
        writer.writeheader()
        writer.writerows(latencies)
    print(f"Saved latency results to {OUTPUT_CSV}")

    # Analyze results
    successful = [r["latency_ms"] for r in latencies if r["status"] == 200]
    failed = [r for r in latencies if r["status"] != 200]

    print(f"Total requests: {len(latencies)}")
    print(f"Successful requests: {len(successful)}")
    print(f"Failed requests: {len(failed)}")

    if successful:
        successful.sort()
        avg = sum(successful)/len(successful)
        median = successful[len(successful)//2]
        print(f"Average latency: {avg:.2f} ms")
        print(f"Median latency: {median:.2f} ms")
        print(f"Max latency: {max(successful):.2f} ms")
        print(f"Min latency: {min(successful):.2f} ms")

        # Plot latency graph
        plt.figure(figsize=(12, 6))
        plt.plot([r["request"] for r in latencies], [r["latency_ms"] for r in latencies], 'o', label="Latency per request")
        plt.axhline(avg, color='r', linestyle='--', label=f"Average ({avg:.2f} ms)")
        plt.axhline(median, color='g', linestyle='--', label=f"Median ({median:.2f} ms)")
        plt.xlabel("Request #")
        plt.ylabel("Latency (ms)")
        plt.title("API Latency per Request")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(LATENCY_PLOT)
        plt.show()
        print(f"Saved latency plot to {LATENCY_PLOT}")

if __name__ == "__main__":
    asyncio.run(main())
