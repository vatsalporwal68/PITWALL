from domain.lap_model import LapModel


def test_calculate_lap_time():
    model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03
    )

    lap_time = model.calculate_lap_time(
        tyre_age=5,
        fuel_load=50
    )

    assert lap_time == 91.9