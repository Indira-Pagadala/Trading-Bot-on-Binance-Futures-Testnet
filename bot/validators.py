def validate_order_input(
    order_type: str,
    side: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
    mark_price: float | None = None,
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    if order_type == "MARKET":
        if price is not None or stop_price is not None:
            raise ValueError("MARKET orders cannot have price or stop price")

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("LIMIT order requires --price")

    if order_type == "STOP-LIMIT":
        if stop_price is None:
            raise ValueError("STOP-LIMIT order requires stop_price")
        if price is None:
            raise ValueError("STOP-LIMIT order requires price")

        if mark_price is None:
            raise ValueError("Internal error: mark price missing")

        if side == "BUY" and stop_price <= mark_price:
            raise ValueError(
                f"STOP-LIMIT BUY stop_price ({stop_price}) must be ABOVE current mark price ({mark_price})"
            )

        if side == "SELL" and stop_price >= mark_price:
            raise ValueError(
                f"STOP-LIMIT SELL stop_price ({stop_price}) must be BELOW current mark price ({mark_price})"
            )
