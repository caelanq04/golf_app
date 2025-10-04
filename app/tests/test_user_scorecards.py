import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.db.users_repo import create_user

client = TestClient(app)


@pytest.fixture
def registered_user():
    username = "testuser"
    email = "testuser@example.com"
    password = "password123"
    user_data = {"username": username, "email": email, "password": password}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    user = response.json()

    login_resp = client.post(
        "/login", json={"username": None, "email": email, "password": password}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    return {"user": user, "token": token}


@pytest.fixture
def new_scorecard(registered_user):
    # user = registered_user["user"]
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/scorecard/9833/White 2019/Standard", headers=headers)
    assert response.status_code == 200
    return response.json(), headers


def test_create_scorecard_authenticated(registered_user):
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/scorecard/9833/White 2019/Standard", headers=headers)
    assert response.status_code == 200
    scorecard = response.json()
    assert scorecard["user_id"] == registered_user["user"]["id"]
    assert scorecard["guest_name"] is None


def test_create_scorecard(new_scorecard):
    scorecard, headers = new_scorecard
    assert "scorecard_id" in scorecard
    assert isinstance(scorecard["holes"], list)
    assert len(scorecard["holes"]) > 0

    assert scorecard["user_id"] is not None
    assert scorecard["guest_name"] is None


def test_update_hole(new_scorecard):
    scorecard, headers = new_scorecard
    scorecard_id = scorecard["scorecard_id"]
    response = client.put(
        f"/scorecard/update/scorecard_id/{scorecard_id}/hole/1/strokes/4/penalties/1/putts/2",
        headers=headers,
    )
    assert response.status_code == 200
    hole = response.json()
    assert hole["hole_number"] == 1
    assert hole["strokes"] == 4
    assert hole["penalties"] == 1
    assert hole["putts"] == 2

    fetch_resp = client.get(f"/scorecard/{scorecard_id}")
    assert fetch_resp.status_code == 200
    updated_card = fetch_resp.json()
    updated_hole = next(h for h in updated_card["holes"] if h["hole_number"] == 1)
    assert updated_hole["strokes"] == 4
    assert updated_hole["penalties"] == 1
    assert updated_hole["putts"] == 2


def test_calculate_totals(new_scorecard):
    scorecard, headers = new_scorecard
    scorecard_id = scorecard["scorecard_id"]
    for hole in range(1, 19):
        client.put(
            f"/scorecard/update/scorecard_id/{scorecard_id}/hole/{hole}/strokes/4/penalties/1/putts/2",
            headers=headers,
        )
    fetch_resp = client.get(f"/scorecard/{scorecard_id}/summary", headers=headers)
    assert fetch_resp.status_code == 200
    summary = fetch_resp.json()
    assert summary["out_par"] == 33
    assert summary["in_par"] == 35
    assert summary["total_par"] == 68
    assert summary["out_score"] == 36
    assert summary["in_score"] == 36
    assert summary["total_score"] == 72
    assert summary["to_par_out_score"] == 3
    assert summary["to_par_in_score"] == 1
    assert summary["to_par_total_score"] == 4


def test_finish_hole(new_scorecard):
    scorecard, headers = new_scorecard
    scorecard_id = scorecard["scorecard_id"]
    response = client.put(f"/scorecard/{scorecard_id}/complete", headers=headers)
    assert response.status_code == 200
    data = response.json()
    scorecard = data["scorecard"]
    summary = data["summary"]
    assert scorecard["finished"]
