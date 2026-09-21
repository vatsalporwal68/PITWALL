from domain.lap_model import LapModel


def test_calculate_lap_time():
    model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08
    )

    lap_time = model.calculate_lap_time(5)

    assert lap_time == 90.4