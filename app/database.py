from typing import Annotated
import os
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends

# DataBase setting section
sql_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")

if sql_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else: connect_args={}

engine = create_engine(sql_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)