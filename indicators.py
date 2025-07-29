import pandas as pd
import ta

def rsi(data, period=14):
    """Calculate RSI"""
    return ta.momentum.RSIIndicator(data['close'], window=period).rsi().iloc[-1]

def ma(data, period=14):
    """Calculate Moving Average"""
    return data['close'].rolling(period).mean().iloc[-1]

def macd(data):
    """Calculate MACD and signal"""
    macd_calc = ta.trend.MACD(data['close'])
    return macd_calc.macd().iloc[-1], macd_calc.macd_signal().iloc[-1]

def adx(data, period=14):
    """Calculate ADX"""
    adx_calc = ta.trend.ADXIndicator(data['high'], data['low'], data['close'], window=period)
    return adx_calc.adx().iloc[-1]

def atr(data, period=14):
    """Calculate Average True Range"""
    atr_calc = ta.volatility.AverageTrueRange(data['high'], data['low'], data['close'], window=period)
    return atr_calc.average_true_range().iloc[-1]
