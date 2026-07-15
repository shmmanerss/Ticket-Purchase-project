from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from event_ticketing.db import Base

class EventDB(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    available_seats = Column(Integer, default=0)
    image_url = Column(String, default="")
