import logging

from .broker import KisBroker, PaperBroker
from .config import load_config
from .risk import RiskManager
from .strategy import MovingAverageCrossStrategy
from .trader import AutoTrader


def build_trader() -> AutoTrader:
    config = load_config()
    if config.trading_mode == "kis":
        broker = KisBroker(
            config.kis_app_key,
            config.kis_app_secret,
            config.kis_account_no,
            config.kis_account_product_code,
        )
    else:
        broker = PaperBroker(config.starting_cash)

    strategy = MovingAverageCrossStrategy(config.fast_window, config.slow_window)
    risk_manager = RiskManager(
        config.max_position_value,
        config.stop_loss_pct,
        config.take_profit_pct,
        config.daily_order_limit,
    )
    return AutoTrader(broker, strategy, risk_manager, config.symbol)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    trader = build_trader()
    trader.run_loop(interval_seconds=1, iterations=10)


if __name__ == "__main__":
    main()
