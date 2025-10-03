from fastapi import APIRouter, HTTPException

from app.models.scorecard import (
    Scorecard,
    GameMode,
    HoleScore,
    ScoreSummary,
    ScorecardFinishedResponse,
)
from app.services.scorecard import create_scorecard, calculate_totals
from app.db.scorecards_repo import (
    insert_scorecard,
    update_scorecard,
    get_scorecard,
    finish_scorecard,
)

router = APIRouter()


@router.get("/{player_name}/{course_id}/{tee_name}/{mode}", response_model=Scorecard)
def create_new_scorecard(
    player_name: str, course_id: int, tee_name: str, mode: GameMode
):
    partial_scorecard = create_scorecard(player_name, course_id, tee_name, mode)
    scorecard_id = insert_scorecard(partial_scorecard)
    return get_scorecard(scorecard_id)


@router.put(
    "/update/scorecard_id/{scorecard_id}/hole/{hole_number}/strokes/{strokes}/penalties/{penalties}/putts/{putts}",
    response_model=HoleScore,
)
def update_hole(
    scorecard_id: int, hole_number: int, strokes: int, penalties: int, putts: int
):
    return update_scorecard(scorecard_id, hole_number, strokes, penalties, putts)


@router.get("/{scorecard_id}", response_model=Scorecard)
def fetch_scorecard(scorecard_id: int):
    scorecard = get_scorecard(scorecard_id)
    if not scorecard:
        raise HTTPException(404, detail="Scorecard not found")
    return scorecard


@router.get("/{scorecard_id}/summary", response_model=ScoreSummary)
def get_summary(scorecard_id: int):
    scorecard = fetch_scorecard(scorecard_id)
    return calculate_totals(scorecard)


@router.put("/{scorecard_id}/complete", response_model=ScorecardFinishedResponse)
def finish_round(scorecard_id: int):
    scorecard = finish_scorecard(scorecard_id)
    summary = get_summary(scorecard_id)
    return ScorecardFinishedResponse(scorecard=scorecard, summary=summary)
