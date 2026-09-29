from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_simulate_strategies_endpoint():
    response = client.post(
        "/simulation/strategies",
        json={
            "race_id": 1,
            "race_entry_id": 1,
            "race_laps": 5,
            "position": 1,
            "fuel_load": 50,
            "fuel_consumption": 2,
            "pit_stop_time": 22.5,
            "base_lap_time": 90.0,
            "tyre_degradation": 0.08,
            "fuel_penalty": 0.03,
            "compound_performance": {
                "Soft": -0.8,
                "Medium": 0.0,
                "Hard": 0.6
            },
            "strategies": [
                {
                    "compounds": ["Medium"],
                    "stint_lengths": [5]
                },
                {
                    "compounds": ["Medium", "Hard"],
                    "stint_lengths": [3, 2]
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["strategies"]) == 2

    assert data["strategies"][0]["strategy_name"] == "Strategy 1"
    assert data["strategies"][0]["total_race_time"] == 458.10
    assert data["strategies"][0]["pit_stops"] == 0

    assert data["strategies"][1]["strategy_name"] == "Strategy 2"
    assert data["strategies"][1]["total_race_time"] == 481.32
    assert data["strategies"][1]["pit_stops"] == 1

    assert data["fastest_strategy"] == "Strategy 1"
    assert data["time_difference"]["Strategy 1"] == 0.0
    assert data["time_difference"]["Strategy 2"] == 23.22