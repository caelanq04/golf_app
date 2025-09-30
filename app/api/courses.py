import os
from os.path import join, dirname
from dotenv import load_dotenv

from fastapi import APIRouter

from app.services.courses import get_course_details

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("GOLF_API_URL")


router = APIRouter()


@router.get("/search/{course_name}")
def get_course_list(course_name: str):
    data = get_course_details(course_name)
    course_list = []
    for course_item in data["courses"]:
        location = course_item.get("location", {})
        course = {
            "Course ID": course_item["id"],
            "Club Name": course_item["club_name"],
            "Address": location.get("address"),
        }

        course_list.append(course)
    return course_list
