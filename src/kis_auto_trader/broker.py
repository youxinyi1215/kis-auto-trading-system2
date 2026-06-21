from dataclasses import dataclass
from random import Random
from typing import Protocol

import requests


@dataclass
class Position:
    symbol: str
    quantity: int = 0
    average_price: float = 0.0


class Broker(Protocol):
    def get_price(self, symbol: str) -> float:
        ...

    def get_history(self, symbol: str, count: int) -> list[float]:
        ...

    def buy(self, symbol: str, quantity: int) -> None:
        ...

    def sell(self, symbol: str, quantity: int) -> None:
        ...

    def get_position(self, symbol: str) -> Position:
        ...

    def get_cash(self) -> float:
        ...


class PaperBroker:
    def __init__(self, starting_cash: float, seed: int = 7) -> None:
        self.cash = starting_cash
        self.random = Random(seed)
        self.prices = [70000 + i * 180 + self.random.randint(-900, 900) for i in range(80)]
        self.positions: dict[str, Position] = {}

    def get_price(self, symbol: str) -> float:
        last_price = self.prices[-1]
        next_price = max(1000, last_price + self.random.randint(-1200, 1200))
        self.prices.append(next_price)
        return float(next_price)

    def get_history(self, symbol: str, count: int) -> list[float]:
        while len(self.prices) < count:
            self.get_price(symbol)
        return self.prices[-count:]

    def buy(self, symbol: str, quantity: int) -> None:
        price = self.get_price(symbol)
        cost = price * quantity
        if cost > self.cash:
            raise ValueError("not enough paper cash")
        position = self.positions.setdefault(symbol, Position(symbol=symbol))
        total_cost = position.average_price * position.quantity + cost
        position.quantity += quantity
        position.average_price = total_cost / position.quantity
        self.cash -= cost

    def sell(self, symbol: str, quantity: int) -> None:
        price = self.get_price(symbol)
        position = self.positions.setdefault(symbol, Position(symbol=symbol))
        if quantity > position.quantity:
            raise ValueError("not enough paper position")
        position.quantity -= quantity
        self.cash += price * quantity
        if position.quantity == 0:
            position.average_price = 0.0

    def get_position(self, symbol: str) -> Position:
        return self.positions.setdefault(symbol, Position(symbol=symbol))

    def get_cash(self) -> float:
        return self.cash


class KisBroker:
    """Minimal KIS adapter skeleton.

    The exact endpoints and transaction IDs should be checked against the current
    KIS Open API documentation before real trading.
    """

    def __init__(self, app_key: str, app_secret: str, account_no: str, product_code: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.account_no = account_no
        self.product_code = product_code
        self.base_url = "https://openapi.koreainvestment.com:9443"
        self.access_token: str | None = None

    def authenticate(self) -> str:
        response = requests.post(
            f"{self.base_url}/oauth2/tokenP",
            json={
                "grant_type": "client_credentials",
                "appkey": self.app_key,
                "appsecret": self.app_secret,
            },
            timeout=10,
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        return self.access_token

    def get_price(self, symbol: str) -> float:
        raise NotImplementedError("connect this method to the KIS quote endpoint")

    def get_history(self, symbol: str, count: int) -> list[float]:
        raise NotImplementedError("connect this method to the KIS daily price endpoint")

    def buy(self, symbol: str, quantity: int) -> None:
        raise NotImplementedError("connect this method to the KIS order endpoint")

    def sell(self, symbol: str, quantity: int) -> None:
        raise NotImplementedError("connect this method to the KIS order endpoint")

    def get_position(self, symbol: str) -> Position:
        raise NotImplementedError("connect this method to the KIS balance endpoint")

    def get_cash(self) -> float:
        raise NotImplementedError("connect this method to the KIS balance endpoint")
