from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from app.database import Player, UpdatePoint, create_db_and_tables
from app.dependencies import get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
	create_db_and_tables()

@app.post("/ranked")
def create_player(*, session: Session = Depends(get_session), player: Player):
	db_player = Player.model_validate(player)
	session.add(db_player)
	session.commit()
	session.refresh(db_player)
	return db_player

@app.get("/ranked/{id}")
def get_rank(*, session: Session = Depends(get_session), id: str):
	player = session.get(Player, id)
	if not player:
		raise HTTPException(status_code=404, detail="Player not found")
	return player

@app.patch("/ranked/{id}")
def update_points(*, session: Session = Depends(get_session), id: str, player: UpdatePoint):
	db_player = session.get(Player, id)
	if not db_player:
		raise HTTPException(status_code=404, detail="Player not found")

	player_data = player.model_dump(exclude_unset=True)
	player_data["points"] += db_player.points

	db_player.sqlmodel_update(player_data)
	session.add(db_player)
	session.commit()
	session.refresh(db_player)
	return db_player
