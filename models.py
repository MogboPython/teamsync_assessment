import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import mysql.connector
import datetime
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=True)
    password = Column(String(150), nullable=False) 

# class TokenTable(Base):
#     __tablename__ = "token"
#     user_id = Column(Integer)
#     access_token = Column(String(450), primary_key=True)
#     refresh_token = Column(String(450),nullable=False)
#     status = Column(Boolean)
#     created_date = Column(DateTime, default=datetime.datetime.now, nullable=False)

class Post(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=True)
    content = Column(Text, nullable=False) 
    author = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

# try:
#     Base.metadata.create_all(engine)
#     print("All tables have been created")
# except Exception as e:
#     print(e)
