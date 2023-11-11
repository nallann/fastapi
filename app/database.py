from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_username}"

#"postgresql://postgres:postgres@localhost/fastapi"
# postgresql://postgres:postgres@localhost:5432/fastapi

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For SQL
# while True:
#     try:
#         conn = psycopg.connect(host="localhost", dbname="fastapi", 
#                             user="postgres", password="postgres", row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)
