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
PORT = int(os.environ.get('PORT', 8000))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=f"https://{os.environ['RAILWAY_STATIC_URL']}/webhook",
    secret_token="YOUR_SECRET_TOKEN"  # 可选，增强安全性
)
# 按钮配置
GROUP_INVITE_HASH = os.environ.get('GROUP_INVITE_HASH', '')
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', '')
CONTACT_USER_ID = os.environ.get('CONTACT_USER_ID', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """带固定菜单的欢迎消息"""
    menu_buttons = ReplyKeyboardMarkup(
        [
            ["📲 小程序", "👥 加入群组"],
            ["📢 进入频道", "📞 联系客服"]
        ],
        resize_keyboard=True,
        input_field_placeholder="请选择功能"
    )
    await update.message.reply_text(
        "欢迎使用！请选择下方菜单：",
        reply_markup=menu_buttons
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理菜单按钮点击"""
    text = update.message.text
    if not text:
        return

    if text == "📲 小程序":
        await update.message.reply_text(
            "点击按钮使用小程序：",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("打开小程序", switch_inline_query_current_chat="")
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
    print(f"⚠️ 错误捕获: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ 操作失败，请稍后再试")

def main():
    """启动机器人（Webhook模式）"""
    app = Application.builder().token(BOT_TOKEN).build()

    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error_handler)

    # Webhook配置
    print(f"🚀 启动Webhook模式，监听端口: {PORT}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        secret_token=os.environ.get('WEBHOOK_SECRET'),
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
