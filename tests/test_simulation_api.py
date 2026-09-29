import pytest
from fastapi.testclient import TestClient

from database import SessionLocal
from main import app
from models import Circuit, Driver, Race, RaceEntry, Team


client = TestClient(app)


@pytest.fixture
def simulation_data():
    db = SessionLocal()

    circuit = Circuit(
        name="Test Circuit",
        country="Test Country"
    )
    db.add(circuit)
    db.flush()

    team = Team(
        name="Test Team",
        nationality="Test"
    )
    db.add(team)
    db.flush()

    driver = Driver(
        name="Test Driver",
        number=1,
        team_id=team.id
    )
    db.add(driver)
    db.flush()

    race = Race(
        name="Test Race",
        circuit_id=circuit.id,
        laps=5
    )
    db.add(race)
    db.flush()

    race_entry = RaceEntry(
        race_id=race.id,
        driver_id=driver.id,
        grid_position=1,
        finishing_position=None,
        points=0.0,
        status="Racing"
    )
    db.add(race_entry)

    db.commit()

    data = {
        "race_id": race.id,
        "race_entry_id": race_entry.id
    }

    yield data

    db.delete(race_entry)
    db.delete(race)
    db.delete(driver)
    db.delete(team)
    db.delete(circuit)

    db.commit()
    db.close()


def test_simulate_strategies_endpoint(simulation_data):
    response = client.post(
        "/simulation/strategies",
        json={
            "race_id": simulation_data["race_id"],
            "race_entry_id": simulation_data["race_entry_id"],
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

def test_rejects_strategy_with_wrong_lap_count():
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
                    "stint_lengths": [3]
                }
            ]
        }
    )

    assert response.status_code == 422


def test_rejects_mismatched_compounds_and_stints():
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
                    "compounds": ["Medium", "Hard"],
                    "stint_lengths": [5]
                }
            ]
        }
    )

    assert response.status_code == 422