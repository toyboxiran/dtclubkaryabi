from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from instagrapi import Client
import os
import logging

# تنظیمات لاگ برای خطایابی
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# لاگین به اینستاگرام
insta_client = Client()
INSTAGRAM_USERNAME = os.getenv("dtclubkaryabi")
INSTAGRAM_PASSWORD = os.getenv("@9126409124ab")

try:
    insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    logging.info("Logged in to Instagram successfully!")
except Exception as e:
    logging.error(f"Error logging in to Instagram: {e}")
    exit(1)

# تابع برای آپلود عکس به استوری
def upload_to_instagram(image_path):
    try:
        insta_client.photo_upload_to_story(image_path, "Uploaded from Telegram")
        logging.info("Photo uploaded to Instagram story!")
    except Exception as e:
        logging.error(f"Error uploading to Instagram: {e}")

# هندلر برای دریافت عکس‌های تلگرام
def handle_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name
    file = update.message.photo[-1].get_file()  # عکس با بهترین کیفیت
    file_path = f"./{file.file_id}.jpg"
    
    # ذخیره عکس محلی
    file.download(file_path)
    logging.info(f"Photo received from {user} in chat {chat_id}, saved as {file_path}")

    # آپلود به اینستاگرام
    upload_to_instagram(file_path)

    # حذف فایل محلی
    os.remove(file_path)
    logging.info(f"Photo {file_path} deleted after upload.")

# تابع اصلی برای راه‌اندازی ربات تلگرام
def main():
    TELEGRAM_BOT_TOKEN = os.getenv("7888584790:AAFUjnDah1EjPaujasrgPUQx9QpgajCOURY")

    if not TELEGRAM_BOT_TOKEN:
        logging.error("Telegram Bot Token is not set!")
        return

    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # هندلر برای عکس‌ها
    photo_handler = MessageHandler(Filters.photo, handle_photo)
    dispatcher.add_handler(photo_handler)

    # شروع ربات
    logging.info("Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
