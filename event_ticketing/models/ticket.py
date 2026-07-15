from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from event_ticketing.db import Base

class TicketDB(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id  = Column(Integer, ForeignKey("users.id"))
    price = Column(Integer)
    reserved_at = Column(DateTime, default=datetime.utcnow)
    paid = Column(Boolean, default=False)
    qr_png = Column(String)
    user  = relationship("UserDB",  back_populates="tickets")  
    event = relationship("EventDB")
    event = relationship("EventDB")          
    user  = relationship("UserDB")
