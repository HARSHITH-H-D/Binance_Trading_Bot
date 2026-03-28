# 🤖 Binance Futures Testnet Trading Bot

A lightweight Python CLI trading bot that places Market, Limit, and Stop-Limit
orders on Binance Futures Testnet (USDT-M) with structured logging and error handling.

---

## 📁 Project Structure
```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Binance API client wrapper
│   ├── orders.py           # Order placement logic + polling
│   ├── validators.py       # Input validation for all order types
│   └── logging_config.py   # Logging setup
├── logs/
│   └── trading_bot.log     # Auto-generated log file
├── cli.py                  # CLI entry point
├── .env                    # API keys (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Steps

### 1. Clone or download the project
```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Register on Binance Futures Testnet

- Go to 👉 https://testnet.binancefuture.com
- Create an account and log in
- Navigate to **API Management**
- Generate your **API Key** and **Secret**
- Enable **Reading** and **Futures** permissions
- Set **IP restriction** to your current IP address

### 5. Add your API keys to `.env`

Create a `.env` file in the root of the project:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> ⚠️ Never share or commit your `.env` file. Add it to `.gitignore`.

---

## 🚀 How to Run

### CLI Arguments Reference

| Argument | Required | Description |
|---|---|---|
| `--symbol` | ✅ Yes | Trading pair (e.g. BTCUSDT) |
| `--side` | ✅ Yes | BUY or SELL |
| `--order_type` | ✅ Yes | MARKET, LIMIT, or STOP_LIMIT |
| `--quantity` | ✅ Yes | Amount to trade (e.g. 0.01) |
| `--price` | ⚠️ Conditional | Required for LIMIT and STOP_LIMIT |
| `--stop_price` | ⚠️ Conditional | Required for STOP_LIMIT only |

---

### ✅ 1. Place a MARKET BUY Order
```bash
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.01
```

**Expected Output:**
```
==================================================
        TRADING BOT — BINANCE FUTURES TESTNET
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.01
==================================================

⏳ Waiting for order to be filled..... ✅ Filled!

==================================================
         ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.01

--------------------------------------------------
         ORDER RESPONSE
--------------------------------------------------
  Order ID   : 13002363705
  Status     : FILLED
  Exec. Qty  : 0.01
  Avg Price  : 84321.50

✅ Order FILLED and placed successfully!
==================================================
```

---

### ✅ 2. Place a LIMIT SELL Order
```bash
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.01 --price 95000
```

> Set price **above** current market price so it stays as NEW (waiting to trigger).

**Expected Output:**
```
==================================================
        TRADING BOT — BINANCE FUTURES TESTNET
==================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : LIMIT
  Quantity   : 0.01
  Limit Price: 95000.0
==================================================

==================================================
         ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : LIMIT
  Quantity   : 0.01
  Limit Price: 95000.0

--------------------------------------------------
         ORDER RESPONSE
--------------------------------------------------
  Order ID   : 13002363800
  Status     : NEW
  Exec. Qty  : 0.000
  Avg Price  : N/A

⚠️  Order accepted but not filled yet (testnet may be slow).
==================================================
```

---

### ✅ 3. Place a STOP-LIMIT SELL Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --order_type STOP_LIMIT --quantity 0.01 --stop_price 78000 --price 77500
```

> Stop price must be **below current market price** for SELL.
> Limit price must be **below stop price**.

**Expected Output:**
```
==================================================
        TRADING BOT — BINANCE FUTURES TESTNET
==================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : STOP_LIMIT
  Quantity   : 0.01
  Limit Price: 77500.0
  Stop Price : 78000.0
==================================================

==================================================
         ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : STOP_LIMIT
  Quantity   : 0.01
  Limit Price: 77500.0
  Stop Price : 78000.0

--------------------------------------------------
         ORDER RESPONSE
--------------------------------------------------
  Order ID   : 13002363999
  Status     : NEW
  Exec. Qty  : 0.000
  Avg Price  : N/A
  Stop Price : 78000.0

✅ Stop-Limit order placed! Waiting for stop price to trigger.
==================================================
```

---

### ❌ Error Examples

**Missing price for LIMIT order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --order_type LIMIT --quantity 0.01
```
```
❌ Validation Error: Price is required for LIMIT orders.
```

**Missing stop_price for STOP_LIMIT order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --order_type STOP_LIMIT --quantity 0.01 --price 77500
```
```
❌ Validation Error: --stop_price is required for STOP_LIMIT orders.
   Example: --stop_price 83000 --price 82500
```

**Invalid side:**
```bash
python cli.py --symbol BTCUSDT --side HOLD --order_type MARKET --quantity 0.01
```
```
❌ Validation Error: Invalid side 'HOLD'. Must be one of: ['BUY', 'SELL']
```

---

## 📄 Log File

All activity is automatically saved to `logs/trading_bot.log`.

**Sample log output covering all 3 order types:**
```
# --- MARKET ORDER ---
2026-03-28 10:15:32 | INFO  | trading_bot | Trading bot started.
2026-03-28 10:15:33 | INFO  | trading_bot | Validation passed | symbol=BTCUSDT side=BUY type=MARKET qty=0.01 price=None stop_price=None
2026-03-28 10:15:33 | INFO  | trading_bot | Placing order | Params: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
2026-03-28 10:15:34 | INFO  | trading_bot | Polling attempt 1/5 | Status: FILLED
2026-03-28 10:15:34 | INFO  | trading_bot | Order FILLED | Final Response: {...}
2026-03-28 10:15:34 | INFO  | trading_bot | Trading bot finished successfully.

# --- LIMIT ORDER ---
2026-03-28 10:18:10 | INFO  | trading_bot | Trading bot started.
2026-03-28 10:18:11 | INFO  | trading_bot | Validation passed | symbol=BTCUSDT side=SELL type=LIMIT qty=0.01 price=95000 stop_price=None
2026-03-28 10:18:11 | INFO  | trading_bot | Placing order | Params: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.01, 'price': 95000}
2026-03-28 10:18:12 | INFO  | trading_bot | Order placed | Initial Response: {'orderId': 13002363800, 'status': 'NEW', ...}
2026-03-28 10:18:12 | INFO  | trading_bot | Trading bot finished successfully.

# --- STOP-LIMIT ORDER ---
2026-03-28 10:21:05 | INFO  | trading_bot | Trading bot started.
2026-03-28 10:21:06 | INFO  | trading_bot | Validation passed | symbol=BTCUSDT side=SELL type=STOP_LIMIT qty=0.01 price=77500 stop_price=78000
2026-03-28 10:21:06 | INFO  | trading_bot | Placing order | Params: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'STOP', 'quantity': 0.01, 'price': 77500, 'stopPrice': 78000}
2026-03-28 10:21:07 | INFO  | trading_bot | Order placed | Initial Response: {'orderId': 13002363999, 'status': 'NEW', ...}
2026-03-28 10:21:07 | INFO  | trading_bot | Trading bot finished successfully.
```

---

## 📦 Requirements
```
python-binance==1.0.19
python-dotenv==1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔒 Security Notes

- Never hardcode API keys in source code
- Always use `.env` file and add it to `.gitignore`
- Enable only **Reading + Futures** permissions on your API key
- Always restrict API access to your **trusted IP address**
- This bot only works on **Testnet** — no real money involved

---

## 📌 Assumptions

- Only **USDT-M Futures** testnet is supported
- Minimum quantity for BTCUSDT is `0.001`
- LIMIT and STOP_LIMIT orders use `timeInForce = GTC` (Good Till Cancelled)
- MARKET orders are polled every 3 seconds up to 5 times (~15 seconds) for FILLED status
- For SELL Stop-Limit: `stop_price` must be greater than `price`
- For BUY Stop-Limit: `stop_price` must be less than `price`
- Python 3.8 or above is required

---

## 🎯 Supported Order Types

| Order Type | Description |
|---|---|
| `MARKET` | Executes immediately at current market price |
| `LIMIT` | Executes when market reaches your set price |
| `STOP_LIMIT` | Triggers a limit order when stop price is hit |

---

## 👤 Author

HARSHITH H D — [github.com/HARSHITH-H-D](https://github.com/HARSHITH-H-D)