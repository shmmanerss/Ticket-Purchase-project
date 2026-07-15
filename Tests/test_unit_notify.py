import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from event_ticketing.notify import send_mail

def test_send_mail():
    try:
        send_mail("test@example.com", "Test Subject", "Message body")
    except Exception:
        assert False, "send_mail raised an exception"
