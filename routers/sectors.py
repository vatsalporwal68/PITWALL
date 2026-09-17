from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Sector as SectorModel
from schemas.sectors import SectorCreate, SectorResponse


router = APIRouter()


@router.get("/sectors", response_model=list[SectorResponse])
def get_sectors(db=Depends(get_db)):
    sectors = db.query(SectorModel).all()
    return sectors


@router.get("/sectors/{sector_id}", response_model=SectorResponse)
def get_sector(sector_id: int, db=Depends(get_db)):
    sector = (
        db.query(SectorModel)
        .filter(SectorModel.id == sector_id)
        .first()
    )

    if sector is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found"
        )

    return sector


@router.post(
    "/sectors",
    response_model=SectorResponse,
    status_code=201
)
def create_sector(
    sector: SectorCreate,
    db=Depends(get_db)
):
    new_sector = SectorModel(
        lap_id=sector.lap_id,
        sector_number=sector.sector_number,
        sector_time=sector.sector_time
    )

    db.add(new_sector)
    db.commit()
    db.refresh(new_sector)

    return new_sector


@router.put(
    "/sectors/{sector_id}",
    response_model=SectorResponse
)
def update_sector(
    sector_id: int,
    updated_sector: SectorCreate,
    db=Depends(get_db)
):
    sector = (
        db.query(SectorModel)
        .filter(SectorModel.id == sector_id)
        .first()
    )

    if sector is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found"
        )

    sector.lap_id = updated_sector.lap_id
    sector.sector_number = updated_sector.sector_number
    sector.sector_time = updated_sector.sector_time

    db.commit()
    db.refresh(sector)

    return sector


@router.delete("/sectors/{sector_id}")
def delete_sector(sector_id: int, db=Depends(get_db)):
    sector = (
        db.query(SectorModel)
        .filter(SectorModel.id == sector_id)
        .first()
    )

    if sector is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found"
        )

    db.delete(sector)
    db.commit()

    return {
        "message": "Sector deleted successfully"
    }
    
@router.get("/sectors/{sector_id}/details")
def get_sector_details(
    sector_id: int,
    db=Depends(get_db)
):
    sector = (
        db.query(SectorModel)
        .filter(SectorModel.id == sector_id)
        .first()
    )

    if sector is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found"
        )

    return {
        "sector_number": sector.sector_number,
        "sector_time": sector.sector_time,
        "lap_id": sector.lap.id,
        "lap_number": sector.lap.lap_number
    }    