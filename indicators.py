import pandas as pd
import ta

def calculate_signals():
    # Example dummy data
    data = pd.DataFrame({
        'close': [1.12, 1.14, 1.13, 1.15, 1.16],
        'high': [1.13, 1.15, 1.14, 1.16, 1.17],
        'low': [1.11, 1.13, 1.12, 1.14, 1.15]
    })

    # Calculate indicators
    data['rsi'] = ta.momentum.RSIIndicator(data['close']).rsi()
    data['adx'] = ta.trend.ADXIndicator(data['high'], data['low'], data['close']).adx()
    data['atr'] = ta.volatility.AverageTrueRange(data['high'], data['low'], data['close']).average_true_range()

    # Generate a simple signal based on RSI
    last_rsi = data['rsi'].iloc[-1]
    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return "HOLD"
