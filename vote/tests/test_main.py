from app.main import app

def test_health():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200


def test_invalid_vote():

    client = app.test_client()

    response = client.post(
        "/api/votes",
        json={
            "option": "invalid"
        }
    )

    assert response.status_code == 400