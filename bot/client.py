import os
import time
import logging
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    def __init__(self):
        self.client = Client(
            api_key=os.getenv("BINANCE_API_KEY"),
            api_secret=os.getenv("BINANCE_API_SECRET"),
            testnet=True,
            requests_params={"timeout": 20},
        )

        self.client.FUTURES_URL = "https://demo-fapi.binance.com/fapi"

        self._sync_timestamp_offset()

    def _sync_timestamp_offset(self) -> None:
        try:
            server_time = self.client.futures_time()
            local_ms = int(time.time() * 1000)
            offset = int(server_time["serverTime"]) - local_ms
            self.client.timestamp_offset = offset
            logger.info(
                "Synced Binance timestamp offset: %sms (serverTime=%s, local=%s)",
                offset,
                server_time["serverTime"],
                local_ms,
            )
        except Exception:
            logger.exception("Failed to sync Binance server time offset")

    def get_mark_price(self, symbol: str) -> float:
        data = self.client.futures_mark_price(symbol=symbol)
        return float(data["markPrice"])

    def place_order(self, **order_params):
        try:
            order_params.setdefault("recvWindow", 5000)

            logger.info(f"Placing order: {order_params}")
            response = self.client.futures_create_order(**order_params)
            logger.info(f"Order response: {response}")
            return response
        except Exception:
            logger.exception("Binance API error")
            raise


def get_client() -> BinanceFuturesClient:
    return BinanceFuturesClient()
