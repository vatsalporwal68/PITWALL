from services.strategy_service import generate_strategies


def test_generate_strategies():
    strategies = generate_strategies(
        race_laps=10,
        compounds=["Soft", "Medium", "Hard"],
        min_stint_laps=2,
        max_stints=3
    )

    assert len(strategies) > 0

    for strategy in strategies:
        assert sum(strategy.stint_lengths) == 10
        assert 1 <= strategy.stint_count <= 3
        assert len(strategy.compounds) == strategy.stint_count

        for stint_length in strategy.stint_lengths:
            assert stint_length >= 2

        for compound in strategy.compounds:
            assert compound in ["Soft", "Medium", "Hard"]

def test_generate_strategies_respects_minimum_stint():
    strategies = generate_strategies(
        race_laps=6,
        compounds=["Soft", "Medium"],
        min_stint_laps=3,
        max_stints=2
    )

    assert len(strategies) > 0

    for strategy in strategies:
        assert strategy.total_laps == 6
        assert strategy.stint_count <= 2

        for stint_length in strategy.stint_lengths:
            assert stint_length >= 3


def test_generate_strategies_with_one_stint():
    strategies = generate_strategies(
        race_laps=10,
        compounds=["Soft", "Medium"],
        min_stint_laps=2,
        max_stints=1
    )

    assert len(strategies) == 2

    for strategy in strategies:
        assert strategy.total_laps == 10
        assert strategy.stint_count == 1
        assert strategy.stint_lengths == [10]

def test_evaluate_strategy():
    from domain.lap_model import LapModel
    from domain.race_state import RaceState
    from domain.strategy import Strategy
    from services.strategy_service import evaluate_strategy

    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=0,
        position=1,
        tyre_compound="Unknown",
        tyre_age=0,
        fuel_load=50,
        status="Running"
    )

    strategy = Strategy(
        compounds=["Medium", "Hard"],
        stint_lengths=[3, 2]
    )

    lap_model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03,
        compound_performance={
            "Soft": -0.8,
            "Medium": 0.0,
            "Hard": 0.6
        }
    )

    result = evaluate_strategy(
        strategy_name="Medium-Hard",
        strategy=strategy,
        state=state,
        lap_model=lap_model,
        fuel_consumption=2,
        pit_stop_time=22.5
    )

    assert result.strategy_name == "Medium-Hard"
    assert result.pit_stops == 1
    assert result.total_race_time == 481.32

    # Original state must not be modified
    assert state.current_lap == 0
    assert state.tyre_age == 0
    assert state.fuel_load == 50                    