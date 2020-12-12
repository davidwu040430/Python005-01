import pymysql
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Date, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User_table(Base):
    __tablename__ = 'user_orm'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    age = Column(SmallInteger())
    birthday = Column(Date())
    gender = Column(String(5))
    education = Column(String(20))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

dburl = "mysql+pymysql://testuser:WyqWys75$@ec2-3-137-159-11.us-east-2.compute.amazonaws.com:3306/testdb"
engine = create_engine(dburl, echo=True, encoding='utf-8')
Base.metadata.create_all(engine)

