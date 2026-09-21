def test_lap_analysis(client):
    response = client.get("/laps/1/analysis")

    assert response.status_code == 200

    data = response.json()

    assert data["lap_id"] == 1
    assert data["lap_time"] == 91.234
    assert data["sector_total"] == 91.234
    assert data["difference"] == 0
    assert data["sector_count"] == 3

def test_lap_analysis_not_found(client):
    response = client.get("/laps/99999/analysis")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Lap not found"

def test_create_lap_validation(client):
    response = client.post(
        "/laps",
        json={
            "race_entry_id": 1,
            "lap_number": -5,
            "lap_time": -100
        }
    )

    assert response.status_code == 422        