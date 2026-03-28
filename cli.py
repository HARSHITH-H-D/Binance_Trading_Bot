# cli.py

import argparse
import sys
from bot.orders import place_order, print_order_summary
from bot.logging_config import setup_logger

logger = setup_logger()


def parse_arguments():
    """Define and parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description="🤖 Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.01

  Limit SELL:
    python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.01 --price 85000

  Stop-Limit SELL:
    python cli.py --symbol BTCUSDT --side SELL --order_type STOP_LIMIT --quantity 0.01 --stop_price 83000 --price 82500
        """
    )

    parser.add_argument("--symbol",     type=str,   required=True,
                        help="Trading pair symbol (e.g., BTCUSDT)")

    parser.add_argument("--side",       type=str,   required=True,
                        choices=["BUY", "SELL"],
                        help="Order side: BUY or SELL")

    parser.add_argument("--order_type", type=str,   required=True,
                        choices=["MARKET", "LIMIT", "STOP_LIMIT"],
                        help="Order type: MARKET, LIMIT, or STOP_LIMIT")

    parser.add_argument("--quantity",   type=float, required=True,
                        help="Quantity to trade (e.g., 0.01)")

    parser.add_argument("--price",      type=float, required=False, default=None,
                        help="Limit price — required for LIMIT and STOP_LIMIT orders")

    parser.add_argument("--stop_price", type=float, required=False, default=None,
                        help="Stop trigger price — required for STOP_LIMIT orders")

    return parser.parse_args()


def main():
    """Main entry point for the trading bot CLI."""

    logger.info("Trading bot started.")

    # Step 1: Parse CLI arguments
    args = parse_arguments()

    # Step 2: Early validation for STOP_LIMIT arguments
    if args.order_type == "STOP_LIMIT" and args.stop_price is None:
        print("\n❌ Validation Error: --stop_price is required for STOP_LIMIT orders.")
        print("   Example: --stop_price 83000 --price 82500")
        sys.exit(1)

    # Step 3: Show what the user entered
    print("\n" + "="*50)
    print("        TRADING BOT — BINANCE FUTURES TESTNET")
    print("="*50)
    print(f"  Symbol     : {args.symbol.upper()}")
    print(f"  Side       : {args.side.upper()}")
    print(f"  Order Type : {args.order_type.upper()}")
    print(f"  Quantity   : {args.quantity}")
    if args.price:
        print(f"  Limit Price: {args.price}")
    if args.stop_price:
        print(f"  Stop Price : {args.stop_price}")
    print("="*50)

    # Step 4: Place the order
    try:
        response = place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )

        # Step 5: Print the result
        print_order_summary(
            params={
                "symbol":     args.symbol.upper(),
                "side":       args.side.upper(),
                "order_type": args.order_type.upper(),
                "quantity":   args.quantity,
                "price":      args.price,
                "stop_price": args.stop_price,
            },
            response=response
        )

        logger.info("Trading bot finished successfully.")
        sys.exit(0)

    except ValueError as e:
        print(f"\n❌ Validation Error: {e}")
        logger.error(f"Validation Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Order Failed: {e}")
        logger.error(f"Order Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()