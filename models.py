from sqlalchemy import Column, Integer, String
from database import Base

class LoveMessage(Base):
    __tablename__ = "love_messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
