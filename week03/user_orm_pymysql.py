import pymysql
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Date, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 用ORM创建表格
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
# Base.metadata.create_all(engine)

# 用pymysql插入三条数据
db = pymysql.connect("ec2-3-137-159-11.us-east-2.compute.amazonaws.com", "testuser", "WyqWys75$", "testdb")
try:
    sql = '''INSERT INTO user_orm (name, age, birthday, gender, education, created_on, updated_on) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    values = (
        ('David Wu', 42, '1978-1-12', 'M', 'Bachelor', datetime.now(), datetime.now()),
        ('Frank Lin', 30, '1990-10-24', 'M', 'Master', datetime.now(), datetime.now()),
        ('Ella Wang', 20, '2000-08-24', 'M', 'High School', datetime.now(), datetime.now())
    )
    with db.cursor() as cursor:
        cursor.executemany(sql, values)
    db.commit()
except Exception as e:
    print(f'Insert error: {e}')
# finally:
#    db.close()

# 用pymysql查询所有的数据
try:
    sql = '''SELECT name, age, birthday, gender, education FROM user_orm'''
    with db.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            print(result)
    db.commit()
except Exception as e:
    print(f'SELECT error: {e}')
finally:
    db.close()




