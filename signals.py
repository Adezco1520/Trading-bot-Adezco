import database
from indicators import rsi, ma, macd, adx, atr
from telegram.ext import Application
import pandas as pd
import requests
import asyncio
import schedule
import time

# Binance API for live data
API_URL = "https://api.binance.com/api/v3/klines?symbol=EURUSDT&interval=1m&limit=100"

def fetch_data(timeframe="1m"):
    """Fetch OHLC data from Binance"""
    url = API_URL.replace("1m", timeframe)
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=['time','open','high','low','close','vol','c1','c2','c3','c4','c5','c6'])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df

async def send_signal(app: Application):
    """Send trading signals to all approved users"""
    users = database.get_approved_users()
    for user_id, strategy, tf in users:
        timeframe = f"{tf}m" if tf else "1m"
        df = fetch_data(timeframe=timeframe)
        signal = None

        if strategy == "rsi":
            val = rsi(df)
            signal = "BUY" if val < 30 else "SELL" if val > 70 else "WAIT"
        elif strategy == "ma":
            ma_val = ma(df)
            signal = "BUY" if df['close'].iloc[-1] > ma_val else "SELL"
        elif strategy == "macd":
            macd_val, signal_val = macd(df)
            signal = "BUY" if macd_val > signal_val else "SELL"
        elif strategy == "adx":
            adx_val = adx(df)
            signal = "STRONG TREND" if adx_val > 25 else "WEAK TREND"
        elif strategy == "atr":
            atr_val = atr(df)
            signal = f"ATR: {atr_val:.5f}"

        if signal:
            await app.bot.send_message(user_id, f"📢 {strategy.upper()} Signal ({tf}m): {signal}")

def start_signal_scheduler(app: Application):
    """Start signal scheduler"""
    schedule.every(1).minutes.do(lambda: asyncio.create_task(send_signal(app)))

    async def scheduler():
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

    asyncio.create_task(scheduler())
