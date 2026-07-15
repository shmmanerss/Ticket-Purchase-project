import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import threading
from event_ticketing.qr import generate_qr_png

def worker():
    for _ in range(10):
        generate_qr_png(f"load-ticket-{_}")

def test_load_simulation():
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
