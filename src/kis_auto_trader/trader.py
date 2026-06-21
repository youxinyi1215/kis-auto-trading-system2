import logging
from time import sleep

from .broker import Broker
from .risk import RiskManager
from .strategy import MovingAverageCrossStrategy, Signal


class AutoTrader:
    def __init__(
        self,
        broker: Broker,
        strategy: MovingAverageCrossStrategy,
        risk_manager: RiskManager,
        symbol: str,
        trade_quantity: int = 1,
    ) -> None:
        self.broker = broker
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.symbol = symbol
        self.trade_quantity = trade_quantity

    def run_once(self) -> None:
        history = self.broker.get_history(self.symbol, self.strategy.slow_window + 1)
        price = self.broker.get_price(self.symbol)
        position = self.broker.get_position(self.symbol)
        decision = self.strategy.decide(history + [price])
        signal = self.risk_manager.apply(decision.signal, price, position)

        logging.info(
            "symbol=%s price=%.2f signal=%s reason=%s cash=%.2f position=%s",
            self.symbol,
            price,
            signal.value,
            decision.reason,
            self.broker.get_cash(),
            position.quantity,
        )

        if signal == Signal.BUY:
            self.broker.buy(self.symbol, self.trade_quantity)
            self.risk_manager.record_order()
            logging.info("BUY order submitted")
        elif signal == Signal.SELL and position.quantity > 0:
            self.broker.sell(self.symbol, min(self.trade_quantity, position.quantity))
            self.risk_manager.record_order()
            logging.info("SELL order submitted")

    def run_loop(self, interval_seconds: int = 5, iterations: int = 5) -> None:
        for _ in range(iterations):
            self.run_once()
            sleep(interval_seconds)
