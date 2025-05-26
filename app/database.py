from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from pydantic import BaseModel

class Player(SQLModel, table=True):
	id: str = Field(primary_key=True)
	username: str
	points: int = Field(default=1000)

class UpdatePoint(SQLModel):
	id: str | None = None
	username: str | None = None
	points: int | None = None

sqlite_file_name = "ranked.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
	SQLModel.metadata.create_all(engine)
