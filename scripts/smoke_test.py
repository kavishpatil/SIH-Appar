"""Post-deploy smoke test: waits for a URL to return HTTP 200 (works on Windows and Linux)."""
import sys
import time
import urllib.request

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/health"
for attempt in range(1, 31):
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            body = resp.read().decode()
            print(f"[smoke] attempt {attempt}: HTTP {resp.status} -> {body}")
            if resp.status == 200:
                sys.exit(0)
    except Exception as exc:
        print(f"[smoke] attempt {attempt}: not ready yet ({exc})")
    time.sleep(2)
print("[smoke] FAILED: service did not become healthy")
sys.exit(1)
