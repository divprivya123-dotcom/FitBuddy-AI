from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(20), nullable=False)
    goal = Column(String(50), nullable=False)
    intensity = Column(String(20), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, default="", nullable=False)
    nutrition_tip = Column(Text, nullable=False)
    feedback = Column(Text, default="", nullable=False)