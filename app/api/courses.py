import os
from os.path import join, dirname
from dotenv import load_dotenv

from fastapi import APIRouter

from app.services.courses import get_course_details
from app.models.courses import CourseSearchResponse

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("GOLF_API_URL")


router = APIRouter()


@router.get("/search/{course_name}", response_model=CourseSearchResponse)
def get_course_list(course_name: str):
    return get_course_details(course_name)
