from models import Stint as StintModel, Lap as LapModel


def analyze_stint(stint_id: int, db):

    stint = (
        db.query(StintModel)
        .filter(StintModel.id == stint_id)
        .first()
    )

    if stint is None:
        return None

    query = (
        db.query(LapModel)
        .filter(
            LapModel.race_entry_id == stint.race_entry_id,
            LapModel.lap_number >= stint.start_lap
        )
    )

    if stint.end_lap is not None:
        query = query.filter(
            LapModel.lap_number <= stint.end_lap
        )

    laps = query.order_by(
        LapModel.lap_number
    ).all()

    lap_times = [
        lap.lap_time
        for lap in laps
    ]

    if not lap_times:
        return {
            "stint_id": stint.id,
            "lap_count": 0,
            "average_lap_time": None,
            "best_lap_time": None,
            "worst_lap_time": None
        }

    return {
        "stint_id": stint.id,
        "lap_count": len(lap_times),
        "average_lap_time": round(
            sum(lap_times) / len(lap_times),
            3
        ),
        "best_lap_time": min(lap_times),
        "worst_lap_time": max(lap_times)
    }