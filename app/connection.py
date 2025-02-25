from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session


# sqlite database connection using sqlmodel
sqlite_file = "user.db"
sqlite_url = f"sqlite:///{sqlite_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]