from domain.race_state import RaceState


def advance_race_state(state: RaceState) -> RaceState:
    state.advance_lap()
    return state