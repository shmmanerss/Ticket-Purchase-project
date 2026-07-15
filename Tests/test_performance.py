import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from event_ticketing.qr import generate_qr_png

def test_qr_generation_speed():
    start = time.time()
    for _ in range(100):
        generate_qr_png(f"ticket-{_}")
    duration = time.time() - start
    assert duration < 5
