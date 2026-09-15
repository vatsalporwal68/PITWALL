from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Team as TeamModel
from schemas.teams import TeamCreate, TeamResponse


router = APIRouter()


@router.get("/teams", response_model=list[TeamResponse])
def get_teams(db=Depends(get_db)):
    teams = db.query(TeamModel).all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db=Depends(get_db)):
    team = (
        db.query(TeamModel)
        .filter(TeamModel.id == team_id)
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team


@router.post(
    "/teams",
    response_model=TeamResponse,
    status_code=201
)
def create_team(team: TeamCreate, db=Depends(get_db)):
    new_team = TeamModel(
        name=team.name,
        nationality=team.nationality
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


@router.put(
    "/teams/{team_id}",
    response_model=TeamResponse
)
def update_team(
    team_id: int,
    updated_team: TeamCreate,
    db=Depends(get_db)
):
    team = (
        db.query(TeamModel)
        .filter(TeamModel.id == team_id)
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    team.name = updated_team.name
    team.nationality = updated_team.nationality

    db.commit()
    db.refresh(team)

    return team


@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db=Depends(get_db)):
    team = (
        db.query(TeamModel)
        .filter(TeamModel.id == team_id)
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    db.delete(team)
    db.commit()

    return {
        "message": "Team deleted successfully"
    }