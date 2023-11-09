import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgres://taskuser:taskpasswd123@database:5432/mydatabase')
metadata = sqlalchemy.MetaData
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class TasksNew(Base):
    __tablename__ = 'NEW_TASKS'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_time = Column(DateTime)
    completed_time = Column(DateTime)
    priority = Column(Integer)
    completed = Column(Integer)


Base.metadata.create_all(engine)
