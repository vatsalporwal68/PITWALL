from models import Lap as LapModel, Sector as SectorModel


def analyze_lap(lap_id: int, db):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        return None

    sectors = (
        db.query(SectorModel)
        .filter(SectorModel.lap_id == lap.id)
        .all()
    )

    sector_total = sum(sector.sector_time for sector in sectors)

    return {
        "lap_id": lap.id,
        "lap_time": lap.lap_time,
        "sector_total": round(sector_total, 3),
        "difference": round(lap.lap_time - sector_total, 3),
        "sector_count": len(sectors)
    }
