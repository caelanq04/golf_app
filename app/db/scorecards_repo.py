from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

from .connection import get_connection
from app.models.scorecard import Scorecard, HoleScore


def insert_scorecard(scorecard: Scorecard) -> int:
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            INSERT INTO scorecards (user_id, guest_name, course_id, course_name, tee_name, mode, finished)
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING id
            ;
            """,
            (
                str(scorecard.user_id) if scorecard.user_id else None,
                scorecard.guest_name,
                scorecard.course_id,
                scorecard.course_name,
                scorecard.tee_name,
                scorecard.mode,
                scorecard.finished,
            ),
        )
        scorecard_id = cur.fetchone()["id"]
        for hole in scorecard.holes:
            cur.execute(
                """
                INSERT INTO hole_scores (scorecard_id, hole_number, par, yardage, handicap)
                VALUES (%s, %s, %s, %s, %s)
                ;
                """,
                (scorecard_id, hole.hole_number, hole.par, hole.yardage, hole.handicap),
            )
        conn.commit()
        return scorecard_id


def get_scorecard(scorecard_id: int) -> Scorecard:
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT * 
            FROM hole_scores
            WHERE scorecard_id = %s
            ;
            """,
            (scorecard_id,),
        )
        holes_data = cur.fetchall()
        holes = [HoleScore.model_validate(hole) for hole in holes_data]

        cur.execute(
            """
            SELECT *
            FROM scorecards
            WHERE id = %s
            ;
            """,
            (scorecard_id,),
        )
        scorecard_data = cur.fetchone()

        if not scorecard_data:
            raise ValueError(f"Scorecard {scorecard_id} not found")

        scorecard = Scorecard(
            scorecard_id=scorecard_data["id"],
            user_id=scorecard_data["user_id"],
            guest_name=scorecard_data["guest_name"],
            course_id=scorecard_data["course_id"],
            course_name=scorecard_data["course_name"],
            tee_name=scorecard_data["tee_name"],
            holes=holes,
            mode=scorecard_data["mode"],
            finished=scorecard_data["finished"],
        )
        return scorecard


def update_scorecard(
    scorecard_id: int, hole_number: int, strokes: int, penalties: int, putts: int
) -> HoleScore:
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            UPDATE hole_scores
            SET strokes=%s, penalties=%s, putts=%s
            WHERE scorecard_id=%s AND hole_number=%s
            RETURNING *
            ;
            """,
            (strokes, penalties, putts, scorecard_id, hole_number),
        )
        updated_row = cur.fetchone()

        if not updated_row:
            raise HTTPException(status_code=404, detail="Scorecard or hole not found")

        conn.commit()
        return HoleScore(
            hole_number=updated_row["hole_number"],
            par=updated_row["par"],
            yardage=updated_row["yardage"],
            handicap=updated_row["handicap"],
            strokes=updated_row["strokes"],
            penalties=updated_row["penalties"],
            putts=updated_row["putts"],
        )


def finish_scorecard(scorecard_id: int):
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            UPDATE scorecards
                SET finished = True
            WHERE id=%s
            RETURNING *
            ;
            """,
            (scorecard_id,),
        )
        scorecard = cur.fetchone()

        if not scorecard:
            raise HTTPException(404, detail="Scorecard not found")
        conn.commit()

        return get_scorecard(scorecard_id)
