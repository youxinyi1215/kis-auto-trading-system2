from dataclasses import dataclass

from .broker import Position
from .strategy import Signal


@dataclass
class RiskState:
    orders_today: int = 0


class RiskManager:
    def __init__(
        self,
        max_position_value: float,
        stop_loss_pct: float,
        take_profit_pct: float,
        daily_order_limit: int,
    ) -> None:
        self.max_position_value = max_position_value
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.daily_order_limit = daily_order_limit
        self.state = RiskState()

    def apply(self, signal: Signal, price: float, position: Position) -> Signal:
        if self.state.orders_today >= self.daily_order_limit:
            return Signal.HOLD

        if position.quantity > 0 and position.average_price > 0:
            pnl_pct = (price - position.average_price) / position.average_price
            if pnl_pct <= -self.stop_loss_pct:
                return Signal.SELL
            if pnl_pct >= self.take_profit_pct:
                return Signal.SELL

        if signal == Signal.BUY and position.quantity * price >= self.max_position_value:
            return Signal.HOLD

        return signal

    def record_order(self) -> None:
        self.state.orders_today += 1
