import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password_hash = Column(String)

def test_end_to_end_user_registration():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = UserDB(id=1, name="Алиса", email="alisa@example.com", phone="1234567890", password_hash="12345")
    session.add(user)
    session.commit()

    saved_user = session.query(UserDB).filter_by(email="alisa@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Алиса"
    assert saved_user.phone == "1234567890"
