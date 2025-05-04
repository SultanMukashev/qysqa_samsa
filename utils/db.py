from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine('postgresql://me:myp4ssw0rd@postgres:5432/master')
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