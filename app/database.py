from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel


DATABASE_URL = "sqlite:///thyroid_cancer_prediction.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
