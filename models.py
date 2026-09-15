from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100))
    circuit_id: Mapped[int] = mapped_column(
        ForeignKey("circuits.id")
    )
    laps: Mapped[int]


class Circuit(Base):
    __tablename__ = "circuits"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100))
    nationality: Mapped[str] = mapped_column(String(100))

class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100))
    number: Mapped[int]
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id")
    )

class RaceEntry(Base):
    __tablename__ = "race_entries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    race_id: Mapped[int] = mapped_column(
        ForeignKey("races.id")
    )
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id")
    )
    grid_position: Mapped[int]
    finishing_position: Mapped[int | None]
    points: Mapped[float]
    status: Mapped[str] = mapped_column(String(50))              