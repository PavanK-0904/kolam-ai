from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///hotel_assistant.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    preferences = Column(Text, default="")

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    sender = Column(String)  # 'guest' or 'bot'
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MemoryLog(Base):
    __tablename__ = 'memory_log'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    memory = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
