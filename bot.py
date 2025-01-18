import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from instagrapi import Client
import requests

# تنظیمات توکن تلگرام و اطلاعات اینستاگرام
TELEGRAM_TOKEN = '7888584790:AAHwsghQpiyINTEBhIR4CT47i5JYfP3we4k'
INSTAGRAM_USERNAME = 'dtclubkaryabi'
INSTAGRAM_PASSWORD = '@9126409124aB'

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ورود به حساب اینستاگرام
instagram_client = Client()
instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# تابع ارسال استوری به اینستاگرام
def send_instagram_story(image_url):
    try:
        # دانلود عکس
        image = requests.get(image_url).content
        with open('temp_image.jpg', 'wb') as f:
            f.write(image)
        
        # ارسال استوری به اینستاگرام
        instagram_client.photo_upload_to_story('temp_image.jpg')
        print("استوری با موفقیت ارسال شد!")
    except Exception as e:
        print(f"خطا در ارسال استوری: {e}")

# تابع برای پردازش عکس‌ها در گروه
def handle_photo(update: Update, context: CallbackContext):
    # بررسی اینکه آیا پیام ارسال شده یک عکس است
    if update.message.photo:
        # دریافت بزرگترین سایز عکس
        photo_file = update.message.photo[-1].get_file()
        photo_url = photo_file.file_url
        
        # ارسال عکس به استوری اینستاگرام
        send_instagram_story(photo_url)

# دستور /start برای اطلاع‌رسانی به کاربر
def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! ربات آماده به کار است.')

# تنظیمات ربات
def main():
    # ایجاد اپدیت کننده و دیسپچر
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ثبت دستورات و پیام‌های ربات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.photo, handle_photo))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
