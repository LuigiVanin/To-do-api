from sqlalchemy import Column, String, Integer, Boolean
from config import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String)
    age = Column(Integer)
    password = Column(String)
    role = Column(String)
    disable = Column(Boolean, default=False)
