from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_lap_analysis():
    response = client.get("/laps/1/analysis")

    assert response.status_code == 200

    data = response.json()

    assert data["lap_id"] == 1
    assert data["lap_time"] == 91.234
    assert data["sector_total"] == 91.234
    assert data["difference"] == 0
    assert data["sector_count"] == 3