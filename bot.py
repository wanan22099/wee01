import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# 环境变量配置
BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'default_secret')
PORT = int(os.environ.get('PORT', 8000))  # Railway 强制要求

# 按钮配置
GROUP_INVITE_HASH = os.environ.get('GROUP_INVITE_HASH', '')
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', '')
CONTACT_USER_ID = os.environ.get('CONTACT_USER_ID', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """带固定菜单的欢迎消息"""
    menu = ReplyKeyboardMarkup(
        [["📲 小程序", "👥 加入群组"], ["📢 进入频道", "📞 联系客服"]],
        resize_keyboard=True,
        input_field_placeholder="请选择功能"
    )
    await update.message.reply_text("欢迎使用！请选择功能：", reply_markup=menu)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理菜单按钮点击"""
    text = update.message.text
    if text == "📲 小程序":
        await update.message.reply_text(
            "点击使用小程序：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("打开", switch_inline_query_current_chat="")
            ]])
        )
    elif text == "👥 加入群组" and GROUP_INVITE_HASH:
        await update.message.reply_text(
            "加入官方群组：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("点击加入", url=f"https://t.me/+{GROUP_INVITE_HASH}")
            ]])
        )
    elif text == "📢 进入频道" and CHANNEL_USERNAME:
        await update.message.reply_text(
            "访问我们的频道：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("点击进入", url=f"https://t.me/{CHANNEL_USERNAME}")
            ]])
        )
    elif text == "📞 联系客服" and CONTACT_USER_ID:
        await update.message.reply_text(
            "联系客服人员：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("点击联系", url=f"tg://user?id={CONTACT_USER_ID}")
            ]])
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """全局错误处理"""
    print(f"⚠️ Error: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ 操作失败，请稍后再试")

def main():
    """启动Webhook服务"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # Webhook配置（适配Railway）
    print(f"🚀 启动Webhook服务，端口: {PORT}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ['RAILWAY_STATIC_URL']}/webhook",
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
