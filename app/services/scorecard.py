from uuid import UUID

from app.models.scorecard import Scorecard, HoleScore, GameMode, ScoreSummary
from app.services.courses import get_course_by_id
from app.db.connection import get_connection


def create_scorecard(
    user_id: UUID | None,
    guest_name: str | None,
    course_id: int,
    tee_name: str,
    mode: str | None,
) -> Scorecard:
    if not user_id and not guest_name:
        raise ValueError("Must provide either a user_id or guest_name")

    if user_id and guest_name:
        raise ValueError("Cannot provide both user_id and guest_name")

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
            new_hole = HoleScore.model_validate({**hole, "hole_number": i})
            holes.append(new_hole)

        else:
            new_hole = HoleScore(**hole.model_dump(), hole_number=i)
            holes.append(new_hole)

    if mode == GameMode.bogey_golf:
        for hole in holes:
            hole.par += 1
    if mode == GameMode.break_100:
        for hole in holes:
            if hole.handicap:
                if hole.handicap <= 9:
                    hole.par += 2
                else:
                    hole.par += 1
    if mode == GameMode.par_90:
        for hole in holes:
            hole.par = 5
    if mode == GameMode.double_bogey_golf:
        for hole in holes:
            hole.par += 2

    scorecard = Scorecard(
        user_id=user_id,
        guest_name=guest_name,
        course_id=course_id,
        course_name=course.club_name,
        tee_name=tee_name,
        holes=holes,
        mode=mode,
    )

    return scorecard


def calculate_totals(scorecard: Scorecard) -> ScoreSummary:
    in_par = 0
    out_par = 0
    in_score = 0
    out_score = 0
    total_score = 0
    to_par_in_score = 0
    to_par_out_score = 0
    to_par_total_score = 0

    for h in scorecard.holes:
        if h.hole_number <= 9:
            in_par += h.par
            if h.strokes is not None:
                in_score += h.strokes
                to_par_in_score += h.strokes - h.par
                total_score += h.strokes
                to_par_total_score += h.strokes - h.par

        else:
            out_par += h.par
            if h.strokes is not None:
                out_score += h.strokes
                to_par_out_score += h.strokes - h.par
                total_score += h.strokes
                to_par_total_score += h.strokes - h.par

    total_par = in_par + out_par

    if scorecard.user_id:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT username FROM users WHERE id =%s;", (scorecard.user_id,)
            )
            username = cur.fetchone()[0]
        name = username
    else:
        name = scorecard.guest_name

    return ScoreSummary(
        scorecard_id=scorecard.scorecard_id,
        name=name,
        in_par=in_par,
        out_par=out_par,
        total_par=total_par,
        in_score=in_score,
        out_score=out_score,
        total_score=total_score,
        to_par_in_score=to_par_in_score,
        to_par_out_score=to_par_out_score,
        to_par_total_score=to_par_total_score,
    )
