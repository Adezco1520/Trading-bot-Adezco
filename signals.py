from telegram import Bot
from indicators import calculate_signals

async def send_trading_signal(bot: Bot, user_id: int, signal: str = None):
    """
    Sends a trading signal to a user.
    If signal is None, it calculates a new one.
    """
    if signal is None:
        signal = calculate_signals()

    message = f"📢 *New Trading Signal*\n\n{signal}"
    await bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
