import requests
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from instagrapi import Client
import os
# تنظیمات توکن تلگرام و اطلاعات اینستاگرام
TELEGRAM_TOKEN = '7888584790:AAHwsghQpiyINTEBhIR4CT47i5JYfP3we4k'
INSTAGRAM_USERNAME = 'dtclubkaryabi'
INSTAGRAM_PASSWORD = '@9126409124aB'


# راه‌اندازی لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# راه‌اندازی کلاینت اینستاگرام
instagram_client = Client()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! من آماده هستم تا عکس‌های شما رو به استوری اینستاگرام ارسال کنم!')

def handle_photo(update: Update, context: CallbackContext) -> None:
    # دریافت عکس
    photo = update.message.photo[-1]  # بزرگترین اندازه عکس
    file = photo.get_file()
    file.download('received_photo.jpg')  # ذخیره عکس در سرور

    # ارسال عکس به مدیر ربات برای تایید
    update.message.reply_text("عکس دریافت شد. در حال ارسال برای تایید...")

    # ارسال عکس به خود مدیر برای تایید
    context.bot.send_photo(chat_id=update.message.from_user.id, photo=open('received_photo.jpg', 'rb'),
                           caption="این عکسی است که دریافت شده. آیا می‌خواهید به استوری اینستاگرام ارسال شود؟")

    # پس از تایید، ارسال عکس به استوری اینستاگرام
    instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    instagram_client.photo_upload_to_story('received_photo.jpg', caption="Story from Telegram")

def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # فرمان‌ها
    dp.add_handler(CommandHandler("start", start))

    # دریافت پیام‌ها و عکس‌ها
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    # راه‌اندازی ربات
    updater.start_polling()

    # منتظر ماندن تا دستورات به پایان برسند
    updater.idle()

if __name__ == '__main__':
    main()
