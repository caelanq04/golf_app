from .api import (
    courses,
    scorecard,
)

from fastapi import FastAPI

app = FastAPI()

app.include_router(courses.router, prefix="/courses")
app.include_router(scorecard.router, prefix="/scorecard")
