from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class TradingConfig:
    trading_mode: str
    symbol: str
    starting_cash: float
    fast_window: int
    slow_window: int
    max_position_value: float
    stop_loss_pct: float
    take_profit_pct: float
    daily_order_limit: int
    kis_app_key: str
    kis_app_secret: str
    kis_account_no: str
    kis_account_product_code: str


def load_config() -> TradingConfig:
    load_dotenv()
    return TradingConfig(
        trading_mode=os.getenv("TRADING_MODE", "paper"),
        symbol=os.getenv("SYMBOL", "005930"),
        starting_cash=float(os.getenv("STARTING_CASH", "1000000")),
        fast_window=int(os.getenv("FAST_WINDOW", "5")),
        slow_window=int(os.getenv("SLOW_WINDOW", "20")),
        max_position_value=float(os.getenv("MAX_POSITION_VALUE", "300000")),
        stop_loss_pct=float(os.getenv("STOP_LOSS_PCT", "0.05")),
        take_profit_pct=float(os.getenv("TAKE_PROFIT_PCT", "0.08")),
        daily_order_limit=int(os.getenv("DAILY_ORDER_LIMIT", "5")),
        kis_app_key=os.getenv("KIS_APP_KEY", ""),
        kis_app_secret=os.getenv("KIS_APP_SECRET", ""),
        kis_account_no=os.getenv("KIS_ACCOUNT_NO", ""),
        kis_account_product_code=os.getenv("KIS_ACCOUNT_PRODUCT_CODE", "01"),
    )
