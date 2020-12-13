import pymysql
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dbconfig import read_db_config
import sys

Base = declarative_base()

# 定义用户表
class User_table(Base):
    __tablename__ = 'user_orm'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), index=True, nullable=False)

# 定义资产表
class Asset_table(Base):
    __tablename__ = 'asset_orm'
    asset_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), index=True, nullable=False; ForeignKey('user_orm.id'))
    balance = Column(Float(), index=True, nullable=False)

# 定义交易审计表
class Transaction_table(Base):
    __tablename__ = 'trx_orm'
    trx_id = Column(Integer(), primary_key=True)
    from_id = Column(Integer(), index=True, nullable=False)
    to_id = Column(Integer(), index=True, nullable=False)
    amount = Column(Float(), index=True, nullable=False)
    create_on = Column(DateTime(), index=True, default=datetime.now)

# 创建数据表
try:
    dbserver = read_db_config()
except Exception as e:
    print(f'Read database configuration error: {e}')
    sys.exit(1)

dburl = "mysql+pymysql://{}:{}@{}:{}/{}".format(dbserver['user'], dbserver['password'], dbserver['host'], dbserver['port'], dbserver['database'])
engine = create_engine(dburl, echo=True)

Base.metadata.create_all(engine)

# 准备session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 准备两个用户，及余额
session.add(User_table(name='张三'))
session.add(User_table(name='李四'))
session.add(Asset_table())

