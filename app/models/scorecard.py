from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class GameMode(str, Enum):
    bogey_golf = "Bogey Golf"
    break_100 = "Break 100"
    par_90 = "Par 90"
    double_bogey_golf = "Double Bogey Golf"
    standard = "Standard"


class HoleScore(BaseModel):
    hole_number: int
    par: int
    yardage: int
    handicap: Optional[int]
    strokes: Optional[int] = None
    penalties: Optional[int] = None
    putts: Optional[int] = None


class Scorecard(BaseModel):
    scorecard_id: Optional[int] = None
    player_name: str
    # guest_1: Optional[str]
    # guest_2: Optional[str]
    # guest_3: Optional[str]
    course_id: int
    course_name: str
    tee_name: str
    holes: List[HoleScore]
    mode: GameMode = GameMode.standard


class ScoreSummary(BaseModel):
    scorecard_id: int
    player_name: str
    in_par: Optional[int] = None
    out_par: Optional[int] = None
    total_par: Optional[int] = None
    in_score: Optional[int] = None
    out_score: Optional[int] = None
    total_score: Optional[int] = None
    to_par_in_score: Optional[int] = None
    to_par_out_score: Optional[int] = None
    to_par_total_score: Optional[int] = None
    # gir_percentage: Optional[int] = None
    # fairways_hit_percentage: Optional[int] = None
    # putts_per_hole_avg: Optional[float] = None
