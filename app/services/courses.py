import os
from os.path import join, dirname
from dotenv import load_dotenv

import httpx

from app.models.courses import CourseSearchResponse, Course

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("GOLF_API_URL")


def get_course_details(course_name: str) -> CourseSearchResponse:
    url = str(URL) + "search"
    headers = {"Authorization": f"Key {API_KEY}"}
    params = {"search_query": course_name}
    response = httpx.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    normalised_courses = [normalise_course_data(c) for c in data["courses"]]

    return CourseSearchResponse(
        courses=[Course.model_validate(c) for c in normalised_courses]
    )


def get_course_by_id(course_id: int) -> Course:
    url = str(URL) + "courses/" + str(course_id)
    headers = {"Authorization": f"Key {API_KEY}"}
    response = httpx.get(url=url, headers=headers)
    response.raise_for_status()
    data = response.json()

    normalised_course = normalise_course_data(data["course"])

    course = Course.model_validate(normalised_course)

    return course


def normalise_course_data(raw_course: dict) -> dict:
    tees = []
    for gender, tee_list in raw_course.get("tees", {}).items():
        for tee in tee_list:
            tee["gender"] = gender
            tees.append(tee)
    raw_course["tees"] = tees
    return raw_course
