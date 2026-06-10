import os 

from dotenv import load_dotenv 
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker 

load_dotenv() # load .env file into python environment 

DATABASE_URL = os.getenv("DATABASE_URL") # find database url variable in loaded .env file

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set. Add DATABASE_URL to your .env file.")

engine = create_engine(DATABASE_URL) # creates engine using the defined URL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # creates the sessions and connects them to the engine 

class Base(DeclarativeBase): # parent class that will be inherited from so that Postgres knows its a table 
    pass

def get_db(): # creates a temp session and returns that session then closes it after done 
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


