from .api import (
    courses,
    scorecard,
    users,
)

from fastapi import FastAPI

app = FastAPI()

app.include_router(courses.router, prefix="/courses")
app.include_router(scorecard.router, prefix="/scorecard")
app.include_router(users.router)
