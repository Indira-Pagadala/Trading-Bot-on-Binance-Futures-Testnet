import logging
from bot.validators import validate_order_input

logger = logging.getLogger(__name__)


def create_order(
    client,
    symbol,
    side,
    order_type,
    quantity,
    price=None,
    stop_price=None,
):
    mark_price = None
    if order_type == "STOP-LIMIT":
        mark = client.client.futures_mark_price(symbol=symbol)
        mark_price = float(mark["markPrice"])
        logger.info(f"Current mark price: {mark_price}")

    validate_order_input(
        order_type=order_type,
        side=side,
        quantity=quantity,
        price=price,
        stop_price=stop_price,
        mark_price=mark_price,
    )

    order_params = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "type": order_type,
    }

    if order_type == "LIMIT":
        order_params["price"] = price
        order_params["timeInForce"] = "GTC"

    if order_type == "STOP-LIMIT":
        order_params["type"] = "STOP"
        order_params["price"] = price
        order_params["stopPrice"] = stop_price
        order_params["timeInForce"] = "GTC"

    logger.info(f"Final order params: {order_params}")
    return client.place_order(**order_params)
