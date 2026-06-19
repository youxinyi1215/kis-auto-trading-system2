# KIS Open API Auto Trading System

This repository is implementation of an automated trading system using the Korea Investment & Securities Open API concept.

The project is intentionally safe by default:

- `paper` mode runs a local simulated broker and never sends real orders.
- `kis` mode is separated behind a broker interface and requires API keys from environment variables.
- Strategies, broker access, scheduling, risk control, and logging are split into small modules.

## Features

- Market data and order interface for paper trading
- Optional KIS Open API adapter structure
- Moving-average crossover strategy
- Risk controls: maximum position size, stop loss, take profit, daily order limit
- Scheduler loop for automated execution
- Clear logs for buy, sell, hold, and risk decisions
- Unit tests for core strategy behavior

## Project Structure

```text
kis-auto-trading-system/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   └── kis_auto_trader/
│       ├── __init__.py
│       ├── broker.py
│       ├── config.py
│       ├── main.py
│       ├── risk.py
│       ├── strategy.py
│       └── trader.py
└── tests/
    └── test_strategy.py
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.kis_auto_trader.main
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.kis_auto_trader.main
```

## Environment Variables

Copy `.env.example` to `.env` if you want to configure the system.

```text
TRADING_MODE=paper
SYMBOL=005930
STARTING_CASH=1000000
FAST_WINDOW=5
SLOW_WINDOW=20
MAX_POSITION_VALUE=300000
STOP_LOSS_PCT=0.05
TAKE_PROFIT_PCT=0.08
DAILY_ORDER_LIMIT=5

KIS_APP_KEY=
KIS_APP_SECRET=
KIS_ACCOUNT_NO=
KIS_ACCOUNT_PRODUCT_CODE=01
```

## How It Works

1. `main.py` loads configuration.
2. `broker.py` provides market data and order execution.
3. `strategy.py` calculates moving averages and creates buy/sell/hold signals.
4. `risk.py` checks position size, stop loss, take profit, and order limits.
5. `trader.py` connects everything into an automated trading loop.

## Strategy

The included strategy uses a simple moving-average crossover:

- Buy signal: short moving average crosses above long moving average.
- Sell signal: short moving average crosses below long moving average.
- Hold signal: no crossover.

This is a basic educational strategy. It is not investment advice.

## KIS Open API Integration Design

The real API adapter should implement the same methods as `PaperBroker`:

- `get_price(symbol)`
- `get_history(symbol, count)`
- `buy(symbol, quantity)`
- `sell(symbol, quantity)`
- `get_position(symbol)`
- `get_cash()`

This keeps the strategy independent from the broker implementation.

## Limitations

- Currently supports only mock trading
- Real-time websocket trading is not implemented yet
- Trading strategy logic is still simple
- Risk management features need improvement

## Future Improvements

- Add RSI and MACD strategies
- Improve automatic trading logic
- Add real-time monitoring dashboard
