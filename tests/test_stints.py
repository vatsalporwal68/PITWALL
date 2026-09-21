from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_stint_analysis():
    response = client.get("/stints/1/analysis")

    assert response.status_code == 200

    data = response.json()

    assert data["stint_id"] == 1
    assert data["lap_count"] == 1
    assert data["average_lap_time"] == 91.234
    assert data["best_lap_time"] == 91.234
    assert data["worst_lap_time"] == 91.234


def test_stint_analysis_not_found():
    response = client.get("/stints/99999/analysis")

    assert response.status_code == 404
    assert response.json()["detail"] == "Stint not found"