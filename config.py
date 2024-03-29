from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from configparser import ConfigParser


config = ConfigParser()
config.read("confi.ini")
# SQL_URL="mysql://name:password@host:port/dbname"
SECRET_KEY = config["SECURITY"]["key"] #"09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = config["SECURITY"]["algorithm"]
EXPIRE_TIME = 30
SQL_URL = config["DATABASE"]["url"]

engine = create_engine(SQL_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

