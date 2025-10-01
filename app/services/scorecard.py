from app.models.scorecard import Scorecard, HoleScore
from app.services.courses import get_course_by_id


def create_scorecard(player_name: str, course_id: int, tee_name: str) -> Scorecard:
    course = get_course_by_id(course_id)
    tee = None
    holes = []
    for t in course.tees:
        if t.tee_name == tee_name:
            tee = t
            break

    if not tee:
        raise ValueError(f"Tee'{tee_name}' not found in course {course.course_name}")

    for i, hole in enumerate(tee.holes, start=1):
        if isinstance(hole, dict):
            new_hole = HoleScore.parse_obj({**hole, "hole_number": i})
            holes.append(new_hole)

        else:
            new_hole = HoleScore(**hole.dict(), hole_number=i)
            holes.append(new_hole)

    scorecard = Scorecard(
        player_name=player_name,
        course_id=course_id,
        course_name=course.club_name,
        tee_name=tee_name,
        holes=holes,
    )

    return scorecard
