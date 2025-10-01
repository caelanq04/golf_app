from fastapi import APIRouter

from app.services.courses import get_course_details, get_course_by_id
from app.models.courses import CourseSearchResponse, Course


router = APIRouter()


@router.get("/search/{course_name}", response_model=CourseSearchResponse)
def get_course_list(course_name: str):
    return get_course_details(course_name)


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    return get_course_by_id(course_id)
