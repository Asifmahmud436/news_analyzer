from sqlalchemy import JSON, DateTime, String, Text, Integer, Column
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(Text, nullable = False)
    body = Column(Text, nullable=False)
    categories = Column(JSON)
    countries = Column(JSON)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now,nullable=False)
    updated_at = Column(DateTime, default=datetime.now,onupdate=datetime.now,nullable=False)

