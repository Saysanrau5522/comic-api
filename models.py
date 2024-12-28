 # Models for comics and users
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Comic(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    panels = Column(Text)  # Store JSON as a string for simplicity
