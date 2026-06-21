from dataclasses import dataclass
from enum import Enum


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass(frozen=True)
class StrategyDecision:
    signal: Signal
    fast_ma: float
    slow_ma: float
    reason: str


def moving_average(values: list[float], window: int) -> float:
    if window <= 0:
        raise ValueError("window must be positive")
    if len(values) < window:
        raise ValueError("not enough values")
    return sum(values[-window:]) / window


class MovingAverageCrossStrategy:
    def __init__(self, fast_window: int, slow_window: int) -> None:
        if fast_window >= slow_window:
            raise ValueError("fast_window must be smaller than slow_window")
        self.fast_window = fast_window
        self.slow_window = slow_window

    def decide(self, history: list[float]) -> StrategyDecision:
        if len(history) < self.slow_window + 1:
            return StrategyDecision(Signal.HOLD, 0.0, 0.0, "not enough history")

        previous = history[:-1]
        prev_fast = moving_average(previous, self.fast_window)
        prev_slow = moving_average(previous, self.slow_window)
        curr_fast = moving_average(history, self.fast_window)
        curr_slow = moving_average(history, self.slow_window)

        if prev_fast <= prev_slow and curr_fast > curr_slow:
            return StrategyDecision(Signal.BUY, curr_fast, curr_slow, "golden cross")
        if prev_fast >= prev_slow and curr_fast < curr_slow:
            return StrategyDecision(Signal.SELL, curr_fast, curr_slow, "dead cross")
        return StrategyDecision(Signal.HOLD, curr_fast, curr_slow, "no crossover")
