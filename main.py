from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import database
from signals import start_signal_scheduler

ADMIN_ID = 1947232401

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

async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pocket_id = update.message.text.strip()

    if database.user_exists(user_id):
        await update.message.reply_text("You already submitted your ID.")
        return

    database.add_user(user_id, pocket_id)
    buttons = [
        [InlineKeyboardButton("Approve ✅", callback_data=f"approve_{user_id}"),
         InlineKeyboardButton("Reject ❌", callback_data=f"reject_{user_id}")]
    ]
    await context.bot.send_message(ADMIN_ID, f"New user request:\nID: {pocket_id}", 
                                   reply_markup=InlineKeyboardMarkup(buttons))
    await update.message.reply_text("✅ Your ID has been submitted. Wait for admin approval.")

async def approve_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, uid = query.data.split("_")
    uid = int(uid)

    if action == "approve":
        database.approve_user(uid)
        await context.bot.send_message(uid, "🎉 Approved! Use /menu to select strategy and timeframe.")
    else:
        await context.bot.send_message(uid, "❌ Rejected.")
    await query.edit_message_text("Action completed.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not database.is_approved(user_id):
        await update.message.reply_text("You are not approved yet.")
        return

    buttons = [
        [InlineKeyboardButton("RSI", callback_data="strategy_rsi"),
         InlineKeyboardButton("MA", callback_data="strategy_ma")],
        [InlineKeyboardButton("MACD", callback_data="strategy_macd"),
         InlineKeyboardButton("ADX", callback_data="strategy_adx")],
        [InlineKeyboardButton("ATR", callback_data="strategy_atr")]
    ]
    await update.message.reply_text("Choose a strategy:", reply_markup=InlineKeyboardMarkup(buttons))

async def select_strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    strategy = query.data.split("_")[1]
    user_id = query.from_user.id
    database.set_strategy(user_id, strategy)

    buttons = [
        [InlineKeyboardButton("1m", callback_data="tf_1"),
         InlineKeyboardButton("5m", callback_data="tf_5"),
         InlineKeyboardButton("15m", callback_data="tf_15")]
    ]
    await query.edit_message_text("Select timeframe:", reply_markup=InlineKeyboardMarkup(buttons))

async def select_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    timeframe = query.data.split("_")[1]
    user_id = query.from_user.id
    database.set_timeframe(user_id, timeframe)
    await query.edit_message_text("✅ Settings saved. You will start receiving signals.")

def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id))
    app.add_handler(CallbackQueryHandler(approve_reject, pattern="^(approve|reject)_"))
    app.add_handler(CallbackQueryHandler(select_strategy, pattern="^strategy_"))
    app.add_handler(CallbackQueryHandler(select_timeframe, pattern="^tf_"))

    start_signal_scheduler(app)

    app.run_polling()

if __name__ == "__main__":
    main()
