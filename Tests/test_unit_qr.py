import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from event_ticketing.qr import generate_qr_png

def test_generate_qr_png():
    data = "ticket-123"
    img = generate_qr_png(data)
    assert img is not None
