from sqlalchemy import Column, Integer, String, Text, text, create_engine, DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
from datetime import datetime

# Maybe, you need to change user name and password.
URL = 'mysql://bookuser:password@localhost/book_data?charset=utf8'
engin = create_engine(URL, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engin)
session = Session()

class Books(Base):
    __tablename__ = "books"
    id_ = Column('id', Integer, primary_key = True)
    name = Column('name', String(255))
    volume = Column('volume', String(255))
    author = Column('author', String(255))
    publisher = Column('publisher', String(255))
    memo = Column('memo', Text())
    create_date = Column('create_date', DATETIME, server_default=text('NOW()'), nullable=False)
    delFlg = Column('del', TINYINT(4), server_default=text('0'), nullable=False)

class BookCategories(Base):
    __tablename__ = "book_categories"
    id_ = Column('id', Integer, primary_key = True)
    code = Column('code', String(255))
    name = Column('name', String(255))

if __name__ == "__main__":
    Base.metadata.create_all(engin)
