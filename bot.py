import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext, filters
from instagrapi import Client
import os

# تنظیمات اولیه
TELEGRAM_TOKEN = '7888584790:AAHwsghQpiyINTEBhIR4CT47i5JYfP3we4k'  # توکن ربات تلگرام
INSTAGRAM_USERNAME = 'dtclubkaryabi'  # نام کاربری اینستاگرام
INSTAGRAM_PASSWORD = '@9126409124aB'  # رمز عبور اینستاگرام

# راه‌اندازی لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# راه‌اندازی کلاینت اینستاگرام
instagram_client = Client()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('سلام! من آماده هستم تا عکس‌های شما رو به استوری اینستاگرام ارسال کنم!')

async def handle_photo(update: Update, context: CallbackContext) -> None:
    # دریافت عکس
    photo = update.message.photo[-1]  # بزرگترین اندازه عکس
    file = await photo.get_file()
    file.download('received_photo.jpg')  # ذخیره عکس در سرور

    # ارسال عکس به مدیر ربات برای تایید
    await update.message.reply_text("عکس دریافت شد. در حال ارسال برای تایید...")

    # ارسال عکس به خود مدیر برای تایید
    await context.bot.send_photo(chat_id=update.message.from_user.id, photo=open('received_photo.jpg', 'rb'),
                                 caption="این عکسی است که دریافت شده. آیا می‌خواهید به استوری اینستاگرام ارسال شود؟")

    # پس از تایید، ارسال عکس به استوری اینستاگرام
    instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    instagram_client.photo_upload_to_story('received_photo.jpg', caption="Story from Telegram")

def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # فرمان‌ها
    application.add_handler(CommandHandler("start", start))

    # دریافت پیام‌ها و عکس‌ها
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # راه‌اندازی ربات
    application.run_polling()

if __name__ == '__main__':
    main()
