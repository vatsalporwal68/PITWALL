from sqlalchemy.orm import Session

from database import engine
from models import Race


with Session(engine) as session:
    races = [
        Race(
            name="Bahrain Grand Prix",
            circuit="Bahrain International Circuit",
            laps=57
        ),
        Race(
            name="Monaco Grand Prix",
            circuit="Circuit de Monaco",
            laps=78
        ),
        Race(
            name="British Grand Prix",
            circuit="Silverstone Circuit",
            laps=52
        )
    ]

    session.add_all(races)
    session.commit()

    print("Races inserted successfully!")