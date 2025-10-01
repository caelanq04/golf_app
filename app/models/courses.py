from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class Location(BaseModel):
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class Hole(BaseModel):
    par: int
    yardage: int
    handicap: int | None = None


class Tee(BaseModel):
    tee_name: str
    gender: Gender
    course_rating: Optional[float]
    slope_rating: Optional[int]
    total_yards: Optional[int]
    number_of_holes: int
    par_total: int
    holes: List[Hole]


class Course(BaseModel):
    id: int
    club_name: str
    course_name: str
    location: Optional[Location]
    tees: List[Tee]


class CourseSearchResponse(BaseModel):
    courses: List[Course]
