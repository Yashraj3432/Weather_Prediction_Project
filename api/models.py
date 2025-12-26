from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from api.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    temp = Column(Float)
    humidity = Column(Float)
    wind = Column(Float)
    result = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
