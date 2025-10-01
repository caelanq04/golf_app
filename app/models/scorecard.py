from pydantic import BaseModel
from typing import Optional, List


class HoleScore(BaseModel):
    hole_number: int
    par: int
    yardage: int
    handicap: Optional[int]
    strokes: Optional[int] = None


class Scorecard(BaseModel):
    player_name: str
    # guest_1: Optional[str]
    # guest_2: Optional[str]
    # guest_3: Optional[str]
    course_id: int
    course_name: str
    tee_name: str
    holes: List[HoleScore]
