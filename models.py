from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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

    circuit: Mapped["Circuit"] = relationship()


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


class Lap(Base):
    __tablename__ = "laps"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    race_entry_id: Mapped[int] = mapped_column(
        ForeignKey("race_entries.id")
    )
    lap_number: Mapped[int]
    lap_time: Mapped[float]


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    lap_id: Mapped[int] = mapped_column(
        ForeignKey("laps.id")
    )
    sector_number: Mapped[int]
    sector_time: Mapped[float]


class TyreCompound(Base):
    __tablename__ = "tyre_compounds"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    tyre_type: Mapped[str] = mapped_column(String(20))


class Stint(Base):
    __tablename__ = "stints"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    race_entry_id: Mapped[int] = mapped_column(
        ForeignKey("race_entries.id")
    )
    tyre_compound_id: Mapped[int] = mapped_column(
        ForeignKey("tyre_compounds.id")
    )
    start_lap: Mapped[int]
    end_lap: Mapped[int | None]
    tyre_age_start: Mapped[int]                              