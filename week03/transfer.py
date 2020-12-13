import pymysql
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey, create_engine
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
    user_id = Column(Integer(), index=True, nullable=False)
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

dburl = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    dbserver['user'], dbserver['password'], dbserver['host'], dbserver['port'], dbserver['database'])
engine = create_engine(dburl, echo=True)

Base.metadata.create_all(engine)

# 准备session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 准备两个用户，及余额
# session.add(User_table(name='张三'))
# session.add(User_table(name='李四'))
# user = session.query(User_table.id).filter(User_table.name=='张三').first()
# session.add(Asset_table(user_id=user.id, balance=150.00))
# user = session.query(User_table.id).filter(User_table.name=='李四').first()
# session.add(Asset_table(user_id=user.id, balance=150.00))
# session.commit()

# 执行转账动作
# from_id = 3, to_id = 4, amount = 100
# 先写入审计表
session.add(Transaction_table(from_id=3, to_id=4, amount=150.0))

# 检查转出方余额，是否小于转出额，如果是，rollback
query = session.query(Asset_table).filter(Asset_table.user_id == 3)
balance = query.first().balance
if balance < 150:
    # 回滚
    session.rollback()
else:
    # 计算新的balance，update
    new_balance = balance - 150
    query.update({Asset_table.balance: new_balance})
    # 计算接收方新的余额
    query = session.query(Asset_table).filter(Asset_table.user_id == 4)
    balance = query.first().balance
    new_balance = balance + 150
    query.update({Asset_table.balance: new_balance})
    # 提交
    session.commit()
