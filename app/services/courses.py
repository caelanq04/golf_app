import os
from os.path import join, dirname
from dotenv import load_dotenv

import httpx

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("GOLF_API_URL")


def get_course_details(course_name: str):
    url = str(URL) + "search"
    headers = {"Authorization": f"Key {API_KEY}"}
    params = {"search_query": course_name}
    response = httpx.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
