from .api import (
    courses,
)

from fastapi import FastAPI

app = FastAPI()

app.include_router(courses.router, prefix="/courses")
