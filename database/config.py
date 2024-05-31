from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import AutoConfig
import os 


config = AutoConfig()

# Синхронный движок для SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///sqlite.db" # config('DATABASE_URL', "postgresql://postgres@localhost:5432/postgres") 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# PostgreSQL для docker-compose
# engine = create_engine("postgresql://username:password@db_host:db_port/db_name")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=engine) 