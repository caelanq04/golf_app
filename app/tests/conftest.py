# import os
# from os.path import join, dirname
# from dotenv import load_dotenv
#
# import httpx
#
# from app.models.courses import CourseSearchResponse, Course
#
# dotenv_path = join(dirname(__file__), "../../.env.test")
# load_dotenv(dotenv_path)
#
# DB_NAME = os.environ.get("DB_NAME")
import os
import pytest
from app.db.connection import get_connection


@pytest.fixture(scope="function", autouse=True)
def use_test_db(monkeypatch):
    monkeypatch.setenv("DB_NAME", "golf_app_test")
    monkeypatch.setenv("DB_PORT", "5433")
    yield
