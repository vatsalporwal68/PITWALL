def test_create_sector_validation(client):
    response = client.post(
        "/sectors",
        json={
            "lap_id": 1,
            "sector_number": 4,
            "sector_time": 30
        }
    )

    assert response.status_code == 422