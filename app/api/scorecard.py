from fastapi import APIRouter

from app.models.scorecard import Scorecard, GameMode
from app.services.scorecard import create_scorecard

router = APIRouter()


@router.get("/{player_name}/{course_id}/{tee_name}/{mode}", response_model=Scorecard)
def create_new_scorecard(
    player_name: str, course_id: int, tee_name: str, mode: GameMode
):
    return create_scorecard(player_name, course_id, tee_name, mode)
