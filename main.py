import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import database
from indicators import calculate_signals
from signals import send_trading_signal

BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789  # Replace with your numeric Telegram ID

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not database.user_exists(user_id):
        await update.message.reply_text(
            "Welcome to the VIP Trading Signal Bot 📊\n\n"
            "👉 First, register with my affiliate link: https://pocket-friends.com/r/hubsllff9j\n"
            "Then send me your Pocket Option ID."
        )
    else:
        await update.message.reply_text("You are already registered. ✅")

# Handle Pocket Option ID
async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pocket_id = update.message.text.strip()
    database.save_user(user_id, pocket_id)
    
    # Notify Admin
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New registration:\nUser ID: {user_id}\nPocket Option ID: {pocket_id}"
    )
    await update.message.reply_text("Your ID has been sent for approval. ✅")

# Admin approval command
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        try:
            user_id = int(context.args[0])
            database.approve_user(user_id)
            await context.bot.send_message(chat_id=user_id, text="✅ You have been approved! Start receiving signals.")
            await update.message.reply_text("User approved successfully.")
        except:
            await update.message.reply_text("⚠️ Usage: /approve <user_id>")
    else:
        await update.message.reply_text("Unauthorized access ❌")

# Signal scheduler
async def start_signal_scheduler(app):
    while True:
        users = database.get_approved_users()
        for user_id in users:
            signal = calculate_signals()
            await send_trading_signal(app.bot, user_id, signal)
        await asyncio.sleep(60)  # Runs every 1 minute

# Main entry
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id))

    # Start scheduler in background
    asyncio.get_event_loop().create_task(start_signal_scheduler(app))

    # Run bot
    app.run_polling()
