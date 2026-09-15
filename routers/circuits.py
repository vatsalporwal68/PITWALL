from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Circuit as CircuitModel
from schemas.circuits import CircuitCreate, CircuitResponse


router = APIRouter()


@router.get("/circuits", response_model=list[CircuitResponse])
def get_circuits(db=Depends(get_db)):
    circuits = db.query(CircuitModel).all()
    return circuits


@router.get("/circuits/{circuit_id}", response_model=CircuitResponse)
def get_circuit(circuit_id: int, db=Depends(get_db)):
    circuit = (
        db.query(CircuitModel)
        .filter(CircuitModel.id == circuit_id)
        .first()
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found"
        )

    return circuit


@router.post("/circuits", response_model=CircuitResponse, status_code=201)
def create_circuit(circuit: CircuitCreate, db=Depends(get_db)):
    new_circuit = CircuitModel(
        name=circuit.name,
        country=circuit.country
    )

    db.add(new_circuit)
    db.commit()
    db.refresh(new_circuit)

    return new_circuit


@router.put("/circuits/{circuit_id}", response_model=CircuitResponse)
def update_circuit(
    circuit_id: int,
    updated_circuit: CircuitCreate,
    db=Depends(get_db)
):
    circuit = (
        db.query(CircuitModel)
        .filter(CircuitModel.id == circuit_id)
        .first()
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found"
        )

    circuit.name = updated_circuit.name
    circuit.country = updated_circuit.country

    db.commit()
    db.refresh(circuit)

    return circuit


@router.delete("/circuits/{circuit_id}")
def delete_circuit(circuit_id: int, db=Depends(get_db)):
    circuit = (
        db.query(CircuitModel)
        .filter(CircuitModel.id == circuit_id)
        .first()
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found"
        )

    db.delete(circuit)
    db.commit()

    return {
        "message": "Circuit deleted successfully",
        "circuit": {
            "id": circuit.id,
            "name": circuit.name,
            "country": circuit.country
        }
    }