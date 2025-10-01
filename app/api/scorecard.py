from fastapi import APIRouter

from app.models.scorecard import Scorecard
from app.services.scorecard import create_scorecard

router = APIRouter()


@router.get("/{player_name}/{course_id}/{tee_name}", response_model=Scorecard)
def create_new_scorecard(player_name: str, course_id: int, tee_name: str):
    return create_scorecard(player_name, course_id, tee_name)
