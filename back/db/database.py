from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('postgresql://me:myp4ssw0rd@46.101.215.10:5432/master')
session = sessionmaker(
    bind = engine,
    class_ = Session,
    expire_on_commit = False,
    autoflush = False
)

def connect_db():
    db = session()
    try: yield db
    finally: db.close()