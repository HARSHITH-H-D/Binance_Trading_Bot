
import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

TESTNET_BASE_URL = "https://testnet.binancefuture.com"

def get_client() -> Client:
    """Create and return a Binance Futures testnet client."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API key or secret not found in environment variables.")
        raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env file.")

    logger.info("Initializing Binance Futures Testnet client...")

    client = Client(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True  # Points to Binance Futures Testnet
    )

    # Override base URL explicitly for USDT-M Futures testnet
    client.FUTURES_URL = TESTNET_BASE_URL + "/fapi"

    logger.info("Client initialized successfully.")
    return client