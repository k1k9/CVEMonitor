import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Getting database credentials from environment variables
username = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
database = os.getenv('MYSQL_DB')

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def create_database():
    Base.metadata.create_all(bind=engine)

# For getting database connection
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
