import ccxt
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize MEXC Exchange
exchange = ccxt.mexc({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True
})

# Bot Configuration
CRYPTO_PAIRS = ['PEPE/USDT', 'DOGE/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT',
                'PYTH/USDT', 'SOL/USDT', 'JUP/USDT', 'MODE/USDT', 'BABYDOGE/USDT',
                'BONK/USDT']
TIMEFRAME = '1m'  # 1-minute for high-speed trading
TRADE_SIZE_PERCENT = 0.1  # 10% of free balance per trade
ATR_MULTIPLIER = 2  # ATR multiplier for trailing stops
TEST_MODE = False
TRADE_COOLDOWN = 10  # Cooldown in seconds for rechecking signals
MAX_TRADES = 100  # Maximum trades per session
MIN_TRANSACTION_SIZE = 3  # Minimum trade value in USDT

portfolio = {'initial_balance': 0, 'current_balance': 0, 'profit_loss': 0}
open_positions = {}

# Logging function


def log_message(message):
    try:
        print(f"{datetime.now()} - {message}")
        with open("trade_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Error logging message: {e}")

# Fetch Spot Balance


def fetch_spot_balance():
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance.get('free', {}).get('USDT', 0)
        return usdt_balance
    except Exception as e:
        log_message(f"Error fetching spot balance: {e}")
        return 0

# Data Fetching and Indicator Calculation


def fetch_data(pair, timeframe, limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(pair, timeframe, limit=limit)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        log_message(f"Error fetching data for {pair}: {e}")
        return None


def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line


def calculate_atr(data, period=14):
    high_low = data["high"] - data["low"]
    high_close = np.abs(data["high"] - data["close"].shift())
    low_close = np.abs(data["low"] - data["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr


def prepare_data(pair):
    data = fetch_data(pair, TIMEFRAME)
    if data is None or len(data) < 26:  # Ensure enough data for indicators
        return None
    macd_line, signal_line = calculate_macd(data)
    data["MACD"] = macd_line
    data["Signal"] = signal_line
    data["ATR"] = calculate_atr(data)
    data["Momentum"] = np.where(
        data["MACD"] > data["Signal"], 1, -1)  # Momentum signal
    return data

# Order Management


def place_order(pair, side, amount):
    if TEST_MODE:
        log_message(f"Simulated {side.upper()} {amount} {pair}")
        return
    try:
        order = exchange.create_order(pair, "market", side, amount)
        log_message(f"{side.upper()} {amount} {pair} executed.")
        return order
    except Exception as e:
        log_message(f"Error placing {side.upper()} order for {pair}: {e}")
        return None


def place_buy_order(pair, amount):
    return place_order(pair, "buy", amount)


def place_sell_order(pair, amount):
    return place_order(pair, "sell", amount)

# Position Management


# Position Management with Dynamic Trailing Stop
def manage_position(pair, price):
    if pair not in open_positions:
        return False
    position = open_positions[pair]
    entry_price = position["entry_price"]
    atr = position["atr"]

    # Adjust the trailing stop dynamically as the price increases
    trailing_stop = position.get(
        "trailing_stop", entry_price - ATR_MULTIPLIER * atr)

    # If the price has moved up significantly, adjust the trailing stop to lock in profits
    if price > entry_price:
        trailing_stop = max(trailing_stop, price - ATR_MULTIPLIER * atr)

    # If the price hits the trailing stop, close the position
    if price <= trailing_stop:
        log_message(
            f"Trailing stop hit for {pair} at {price}. Closing position.")
        place_sell_order(pair, position["amount"])
        open_positions.pop(pair, None)
        return True

    # Save the new trailing stop value to the position
    open_positions[pair]["trailing_stop"] = trailing_stop
    return False


# Trading Logic


def calculate_trade_size(balance, current_price):
    trade_size = (balance * TRADE_SIZE_PERCENT) / current_price
    trade_value_in_usdt = trade_size * current_price
    if trade_value_in_usdt < MIN_TRANSACTION_SIZE:
        trade_size = MIN_TRANSACTION_SIZE / current_price
    return max(trade_size, 0)


def trade(pair, data):
    latest = data.iloc[-1]
    current_price = latest["close"]

    if pair in open_positions:
        current_price = latest["close"]
        manage_position(pair, current_price)
        return

    if latest["Momentum"] == 1:  # Buy Signal
        balance = fetch_spot_balance()
        trade_size = calculate_trade_size(balance, current_price)

        if trade_size <= 0:
            log_message(f"Insufficient balance to place order for {pair}")
            return

        place_buy_order(pair, trade_size)
        open_positions[pair] = {
            "entry_price": current_price,
            "amount": trade_size,
            "atr": latest["ATR"]
        }
        log_message(f"Opened position for {pair}: {open_positions[pair]}")


# Bot Main Loop
if __name__ == "__main__":
    log_message("Starting spot trading bot.")
    portfolio["initial_balance"] = fetch_spot_balance()

    while len(open_positions) < MAX_TRADES:
        for pair in CRYPTO_PAIRS:
            try:
                data = prepare_data(pair)
                if data is not None:
                    trade(pair, data)
            except Exception as e:
                log_message(f"Error processing {pair}: {e}")
        time.sleep(TRADE_COOLDOWN)
