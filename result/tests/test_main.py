from app.main import app

def test_health_without_database():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code in (200, 503)


def test_results_endpoint():

    client = app.test_client()

    response = client.get("/api/results")

    assert response.status_code in (200, 503)