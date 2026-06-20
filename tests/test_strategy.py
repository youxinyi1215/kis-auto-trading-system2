from src.kis_auto_trader.strategy import MovingAverageCrossStrategy, Signal, moving_average


def test_moving_average() -> None:
    assert moving_average([1, 2, 3, 4], 2) == 3.5


def test_strategy_buy_signal() -> None:
    strategy = MovingAverageCrossStrategy(fast_window=2, slow_window=3)
    decision = strategy.decide([10, 5, 5, 9])
    assert decision.signal == Signal.BUY


def test_strategy_hold_when_no_crossover() -> None:
    strategy = MovingAverageCrossStrategy(fast_window=2, slow_window=3)
    decision = strategy.decide([10, 11, 12, 13])
    assert decision.signal == Signal.HOLD
