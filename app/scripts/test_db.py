import os
from os.path import join, dirname

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

# conn = psycopg2.connect(DATABASE_URL)
conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT now() as when;")
print(cur.fetchone())
cur.close()
conn.close()
