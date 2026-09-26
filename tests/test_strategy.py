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