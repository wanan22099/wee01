import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_URL = os.environ['RAILWAY_STATIC_URL'] + '/webhook'  # Railway自动提供的域名
PORT = int(os.environ.get('PORT', 8000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = ReplyKeyboardMarkup(
        [["📲 小程序", "👥 群组"], ["📢 频道", "📞 客服"]],
        resize_keyboard=True
    )
    await update.message.reply_text("请选择功能：", reply_markup=menu)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📲 小程序":
        await update.message.reply_text(
            "点击使用小程序：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("打开", switch_inline_query_current_chat="")
            ]])
        )
    # 其他按钮处理（参考之前代码）

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Webhook模式配置
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        secret_token=os.environ.get('WEBHOOK_SECRET'),  # 可选安全令牌
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
