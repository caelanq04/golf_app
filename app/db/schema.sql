CREATE TABLE IF NOT EXISTS scorecards (
	id SERIAL PRIMARY KEY,
	player_name TEXT NOT NULL,
	course_id INT NOT NULL,
	course_name TEXT NOT NULL,
	tee_name TEXT NOT NULL,
	mode TEXT,
	created_at TIMESTAMP DEFAULT NOW(),
	updated_at TIMESTAMP DEFAULT NOW(),
	finished BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS hole_scores(
	id SERIAL PRIMARY KEY,
	scorecard_id INT NOT NULL REFERENCES scorecards(id) ON DELETE CASCADE,
	hole_number INT NOT NULL,
	par INT NOT NULL,
	yardage INT NOT NULL,
	handicap INT,
	strokes INT,
	penalties INT,
	putts INT
);

CREATE INDEX IF NOT EXISTS idx_hole_scores_scorecard ON hole_scores(scorecard_id);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp"

CREATE TABLE IF NOT EXISTS users(
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	username TEXT UNIQUE NOT NULL,
	email TEXT UNIQUE NOT NULL,
	hashed_password TEXT UNIQUE,
	created_at TIMESTAMP DEFAULT NOW()
);
