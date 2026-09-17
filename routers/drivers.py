from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Driver as DriverModel
from schemas.drivers import DriverCreate, DriverResponse


router = APIRouter()


@router.get("/drivers", response_model=list[DriverResponse])
def get_drivers(db=Depends(get_db)):
    drivers = db.query(DriverModel).all()
    return drivers


@router.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db=Depends(get_db)):
    driver = (
        db.query(DriverModel)
        .filter(DriverModel.id == driver_id)
        .first()
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver


@router.post(
    "/drivers",
    response_model=DriverResponse,
    status_code=201
)
def create_driver(driver: DriverCreate, db=Depends(get_db)):
    new_driver = DriverModel(
        name=driver.name,
        number=driver.number,
        team_id=driver.team_id
    )

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return new_driver


@router.put(
    "/drivers/{driver_id}",
    response_model=DriverResponse
)
def update_driver(
    driver_id: int,
    updated_driver: DriverCreate,
    db=Depends(get_db)
):
    driver = (
        db.query(DriverModel)
        .filter(DriverModel.id == driver_id)
        .first()
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.name = updated_driver.name
    driver.number = updated_driver.number
    driver.team_id = updated_driver.team_id

    db.commit()
    db.refresh(driver)

    return driver


@router.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db=Depends(get_db)):
    driver = (
        db.query(DriverModel)
        .filter(DriverModel.id == driver_id)
        .first()
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully"
    }

@router.get("/drivers/{driver_id}/team")
def get_driver_team(driver_id: int, db=Depends(get_db)):

    driver = (
        db.query(DriverModel)
        .filter(DriverModel.id == driver_id)
        .first()
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return {
        "driver": driver.name,
        "team": driver.team.name,
        "nationality": driver.team.nationality
    }
