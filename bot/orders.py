# bot/orders.py

import time
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_client
from bot.validators import validate_inputs
from bot.logging_config import setup_logger

logger = setup_logger()

MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds


def place_order(symbol: str, side: str, order_type: str, quantity: float,
                price: float = None, stop_price: float = None) -> dict:
    """Main function to place a market, limit, or stop-limit order."""

    # Step 1: Validate inputs
    symbol, side, order_type, quantity, price, stop_price = validate_inputs(
        symbol, side, order_type, quantity, price, stop_price
    )

    # Step 2: Initialize client
    client = get_client()

    # Step 3: Build order parameters
    order_params = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
    }

    if order_type == "MARKET":
        order_params["type"] = "MARKET"

    elif order_type == "LIMIT":
        order_params["type"] = "LIMIT"
        order_params["price"] = price
        order_params["timeInForce"] = "GTC"

    elif order_type == "STOP_LIMIT":
        order_params["type"] = "STOP"          # Binance uses "STOP" for Stop-Limit
        order_params["price"] = price          # Limit price (execute at this price)
        order_params["stopPrice"] = stop_price # Trigger price (activates the order)
        order_params["timeInForce"] = "GTC"

    # Step 4: Log the request
    logger.info(f"Placing order | Params: {order_params}")

    # Step 5: Send order to Binance
    try:
        response = client.futures_create_order(**order_params)
        logger.info(f"Order placed | Initial Response: {response}")

        # Step 6: Poll for FILLED status (only for MARKET orders)
        if order_type == "MARKET":
            response = wait_for_fill(client, symbol, response["orderId"])

        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Error | Code: {e.code} | Message: {e.message}")
        raise

    except BinanceRequestException as e:
        logger.error(f"Network/Request Error | {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error | {str(e)}")
        raise


def wait_for_fill(client, symbol: str, order_id: int) -> dict:
    """Poll Binance every RETRY_DELAY seconds until MARKET order is FILLED."""

    print("\n⏳ Waiting for order to be filled", end="", flush=True)

    for attempt in range(1, MAX_RETRIES + 1):
        print(".", end="", flush=True)
        time.sleep(RETRY_DELAY)

        updated = client.futures_get_order(symbol=symbol, orderId=order_id)
        status = updated.get("status")

        logger.info(f"Polling attempt {attempt}/{MAX_RETRIES} | Status: {status}")

        if status == "FILLED":
            print(" ✅ Filled!\n")
            logger.info(f"Order FILLED | Final Response: {updated}")
            return updated

    print(" ⚠️ Not filled yet (testnet may be slow)\n")
    logger.warning(f"Order not FILLED after {MAX_RETRIES} retries.")
    return updated

def print_order_summary(params: dict, response: dict):
    """Print a clean summary of the order request and response."""

    print("\n" + "="*50)
    print("         ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"  Symbol     : {params.get('symbol')}")
    print(f"  Side       : {params.get('side')}")
    print(f"  Order Type : {params.get('order_type')}")
    print(f"  Quantity   : {params.get('quantity')}")
    if params.get("price"):
        print(f"  Limit Price: {params.get('price')}")
    if params.get("stop_price"):
        print(f"  Stop Price : {params.get('stop_price')}")

    print("\n" + "-"*50)
    print("         ORDER RESPONSE")
    print("-"*50)

    # Fix: Handle both regular and algo order response formats
    is_stop_limit = params.get("order_type") == "STOP_LIMIT"

    if is_stop_limit:
        # STOP_LIMIT returns algoId and algoStatus
        print(f"  Order ID   : {response.get('algoId')}")
        print(f"  Status     : {response.get('algoStatus')}")
        print(f"  Quantity   : {response.get('quantity')}")
        print(f"  Limit Price: {response.get('price', 'N/A')}")
        print(f"  Stop Price : {response.get('triggerPrice', 'N/A')}")
    else:
        # MARKET and LIMIT return orderId and status
        print(f"  Order ID   : {response.get('orderId')}")
        print(f"  Status     : {response.get('status')}")
        print(f"  Exec. Qty  : {response.get('executedQty')}")
        print(f"  Avg Price  : {response.get('avgPrice', 'N/A')}")

    status = response.get("algoStatus") if is_stop_limit else response.get("status")

    if status == "FILLED":
        print("\n✅ Order FILLED and placed successfully!")
    elif status == "NEW":
        if is_stop_limit:
            print("\n✅ Stop-Limit order placed! Waiting for stop price to trigger.")
        else:
            print("\n⚠️  Order accepted but not filled yet (testnet may be slow).")
    else:
        print(f"\n⚠️  Order status: {status}")

    print("="*50 + "\n")