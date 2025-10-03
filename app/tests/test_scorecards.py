import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from app.main import app

client = TestClient(app)


@pytest.fixture
def new_scorecard():
    user_id = uuid4()
    course_id = 9833
    tee_name = "White 2019"
    mode = "Standard"

    response = client.get(f"/scorecard/{user_id}/{course_id}/{tee_name}/{mode}")
    assert response.status_code == 200
    return response.json(), user_id


def test_create_scorecard(new_scorecard):
    scorecard, user_id = new_scorecard
    assert "scorecard_id" in new_scorecard
    assert new_scorecard["user_id"] == user_id
    assert isinstance(new_scorecard["holes"], list)
    assert len(new_scorecard["holes"]) > 0


def test_update_hole(new_scorecard):
    scorecard_id = new_scorecard["scorecard_id"]
    response = client.put(
        f"/scorecard/update/scorecard_id/{scorecard_id}/hole/1/strokes/4/penalties/1/putts/2"
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
