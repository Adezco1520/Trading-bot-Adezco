import pandas as pd
import ta

# RSI function
def rsi(data):
    return ta.momentum.RSIIndicator(data['close']).rsi()

# Moving Average
def ma(data, window=14):
    return data['close'].rolling(window=window).mean()

# MACD
def macd(data):
    macd_indicator = ta.trend.MACD(data['close'])
    return macd_indicator.macd(), macd_indicator.macd_signal()

# ADX
def adx(data):
    return ta.trend.ADXIndicator(data['high'], data['low'], data['close']).adx()

# ATR
def atr(data):
    return ta.volatility.AverageTrueRange(data['high'], data['low'], data['close']).average_true_range()

# Main signal generator
def calculate_signals():
    data = pd.DataFrame({
        'close': [1.12, 1.14, 1.13, 1.15, 1.16],
        'high': [1.13, 1.15, 1.14, 1.16, 1.17],
        'low': [1.11, 1.13, 1.12, 1.14, 1.15]
    })

    last_rsi = rsi(data).iloc[-1]
    last_adx = adx(data).iloc[-1]
    last_atr = atr(data).iloc[-1]

    if last_rsi < 30 and last_adx > 25:
        return f"BUY 📈\nRSI: {last_rsi:.2f}\nADX: {last_adx:.2f}\nATR: {last_atr:.4f}"
    elif last_rsi > 70 and last_adx > 25:
        return f"SELL 📉\nRSI: {last_rsi:.2f}\nADX: {last_adx:.2f}\nATR: {last_atr:.4f}"
    else:
        return f"HOLD 🤝\nRSI: {last_rsi:.2f}\nADX: {last_adx:.2f}\nATR: {last_atr:.4f}"
