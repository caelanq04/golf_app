import os
from os.path import join, dirname

from dotenv import load_dotenv
import psycopg2
# from psycopg2.extras import RealDictCursor

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")


# conn = psycopg2.connect(DATABASE_URL)
def get_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
    )
    return conn


# def fetch_scorecard(scorecard_id):
#     with get_connection() as conn:
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#         cur.execute("SELECT * FROM scorecards WHERE id = %s", (scorecard_id,))
#         scorecard = cur.fetchone()
#         if not scorecard:
#             return None
#         cur.execute(
#             "SELECT * FROM hole_scores WHERE scorecard_id = %s ORDER BY hole_number",
#             (scorecard_id),
#         )
#         holes = cur.fetchall()
#         scorecard["holes"] = holes
#         return scorecard
