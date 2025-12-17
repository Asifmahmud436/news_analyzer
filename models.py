from sqlalchemy import JSON, DateTime, Text, Integer, Column
from datetime import datetime
from database import Base

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(Text, nullable = False)
    body = Column(Text, nullable=False)
    categories = Column(JSON)
    created_at = Column(DateTime, default=datetime.now,nullable=False)
    updated_at = Column(DateTime, default=datetime.now,onupdate=datetime.now,nullable=False)

