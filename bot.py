import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters

# 替换为你的 Telegram Bot Token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# 替换为你的 Railway 部署的 Webhook URL
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# 替换为你的实际信息
MINI_APP_URL = 'https://t.me/your_mini_app'
GROUP_URL = 'https://t.me/your_group'
CHANNEL_URL = 'https://t.me/your_channel'
CONTACT_URL = 'https://t.me/your_contact'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("内置小程序", url=MINI_APP_URL)],
        [InlineKeyboardButton("群组", url=GROUP_URL)],
        [InlineKeyboardButton("频道", url=CHANNEL_URL)],
        [InlineKeyboardButton("联系人", url=CONTACT_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('请选择一个操作：', reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("你发送了一条消息！")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 设置 Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8000)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )


if __name__ == '__main__':
    main()
