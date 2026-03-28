# bot/validators.py

from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_LIMIT"]


def validate_inputs(symbol: str, side: str, order_type: str, quantity: float,
                    price: float = None, stop_price: float = None):
    """Validate all user inputs before placing an order."""

    # Validate symbol
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT).")
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        logger.warning(f"Symbol '{symbol}' does not end with USDT. Proceeding anyway.")

    # Validate side
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {VALID_SIDES}")

    # Validate order type
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {VALID_ORDER_TYPES}")

    # Validate quantity
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError(f"Quantity must be a positive number. Got: {quantity}")

    # Validate price for LIMIT orders
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f"Price must be a positive number. Got: {price}")

    # Validate stop_price and price for STOP_LIMIT orders
    if order_type == "STOP_LIMIT":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders.")
        if not isinstance(stop_price, (int, float)) or stop_price <= 0:
            raise ValueError(f"Stop price must be a positive number. Got: {stop_price}")
        if price is None:
            raise ValueError("Limit price is required for STOP_LIMIT orders.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f"Limit price must be a positive number. Got: {price}")

        # Logical validation for SELL Stop-Limit
        if side == "SELL" and stop_price <= price:
            raise ValueError(
                f"For SELL Stop-Limit: stop_price ({stop_price}) must be "
                f"greater than limit price ({price})."
            )

        # Logical validation for BUY Stop-Limit
        if side == "BUY" and stop_price >= price:
            raise ValueError(
                f"For BUY Stop-Limit: stop_price ({stop_price}) must be "
                f"less than limit price ({price})."
            )

    logger.info(
        f"Validation passed | symbol={symbol} side={side} type={order_type} "
        f"qty={quantity} price={price} stop_price={stop_price}"
    )

    return symbol, side, order_type, quantity, price, stop_price