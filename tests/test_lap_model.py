from domain.lap_model import LapModel


def test_calculate_lap_time():
    model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03,
        compound_performance={
            "Soft": -0.8,
            "Medium": 0.0,
            "Hard": 0.6
        }
    )

    lap_time = model.calculate_lap_time(
        tyre_age=5,
        fuel_load=50,
        tyre_compound="Medium"
    )

    assert lap_time == 91.9


def test_soft_is_faster_than_medium():
    model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03,
        compound_performance={
            "Soft": -0.8,
            "Medium": 0.0,
            "Hard": 0.6
        }
    )

    soft_time = model.calculate_lap_time(
        tyre_age=0,
        fuel_load=50,
        tyre_compound="Soft"
    )

    medium_time = model.calculate_lap_time(
        tyre_age=0,
        fuel_load=50,
        tyre_compound="Medium"
    )

    assert soft_time < medium_time


def test_hard_is_slower_than_medium():
    model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03,
        compound_performance={
            "Soft": -0.8,
            "Medium": 0.0,
            "Hard": 0.6
        }
    )

    hard_time = model.calculate_lap_time(
        tyre_age=0,
        fuel_load=50,
        tyre_compound="Hard"
    )

    medium_time = model.calculate_lap_time(
        tyre_age=0,
        fuel_load=50,
        tyre_compound="Medium"
    )

    assert hard_time > medium_time