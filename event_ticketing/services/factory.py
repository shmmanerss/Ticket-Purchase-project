# event_ticketing/services/factory.py

from datetime import datetime
from event_ticketing.db import SessionLocal
from event_ticketing.models.ticket import TicketDB
from event_ticketing.models.event import EventDB

class TicketFactory:
    @staticmethod
    def create(event_id: int, user_id: int, price: int = 50) -> TicketDB:
        with SessionLocal() as db:
            # Шаг 1: забираем событие и уменьшаем кол-во мест
            ev = db.get(EventDB, event_id)
            if ev.available_seats <= 0:
                raise Exception("Sold out")
            ev.available_seats -= 1

            # Шаг 2: создаем объект билета
            ticket = TicketDB(
                event_id=event_id,
                user_id=user_id,
                price=price,
                reserved_at=datetime.now()
            )
            db.add(ticket)
            db.commit()
            db.refresh(ticket)  
            return ticket
