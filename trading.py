import os
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

# Initialize Alpaca client only if credentials are available
alpaca = None
if API_KEY and SECRET_KEY:
    try:
        alpaca = REST(API_KEY, SECRET_KEY, BASE_URL)
    except Exception as e:
        print(f"Warning: Failed to initialize Alpaca client: {e}")
        alpaca = None

def get_latest_price(symbol: str):
    """
    Get the latest market price for a given symbol.
    """
    if alpaca is None:
        raise ValueError("Alpaca client not initialized. Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables.")
    try:
        barset = alpaca.get_bars(symbol, TimeFrame.Minute, limit=1)
        if barset:
            return barset[-1].c  # Close price
        return None
    except Exception as e:
        print(f"Error fetching latest price for {symbol}: {e}")
        return None

def generate_trade_signal(symbol: str, account_size: float = 1000):
    """
    Simple strategy: for demonstration, return buy/sell based on last price movement.
    """
    if alpaca is None:
        raise ValueError("Alpaca client not initialized. Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables.")
    try:
        barset = alpaca.get_bars(symbol, TimeFrame.Minute, limit=5)
        if len(barset) < 2:
            return None
    except Exception as e:
        print(f"Error fetching bars for {symbol}: {e}")
        return None

    close_prices = np.array([bar.c for bar in barset])
    direction = "buy" if close_prices[-1] > close_prices[-2] else "sell"
    entry_price = close_prices[-1]
    stop_loss = entry_price * 0.995 if direction == "buy" else entry_price * 1.005
    take_profit = entry_price * 1.01 if direction == "buy" else entry_price * 0.99

    # Determine lot size (simple risk-based: 1% of account per trade)
    risk_per_trade = 0.01 * account_size
    risk_per_unit = abs(entry_price - stop_loss)
    quantity = max(int(risk_per_trade / risk_per_unit), 1)

    return {
        "symbol": symbol,
        "direction": direction,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "quantity": quantity
    }
