from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from instagrapi import Client  # کتابخانه اینستاگرام برای ارسال استوری

# توکن تلگرام و اطلاعات اینستاگرام
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
INSTAGRAM_USERNAME = 'YOUR_INSTAGRAM_USERNAME'
INSTAGRAM_PASSWORD = 'YOUR_INSTAGRAM_PASSWORD'

# راه‌اندازی ربات اینستاگرام
instagram_client = Client()
instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# تابع ارسال استوری به اینستاگرام
def send_instagram_story(photo_path):
    instagram_client.photo_upload(photo_path, caption="Your caption")

# تابع شروع ربات تلگرام
async def start(update: Update, context):
    await update.message.reply("سلام! ربات من آماده است.")

# تابع ارسال استوری به اینستاگرام
async def send_story(update: Update, context):
    # در اینجا می‌توانید مسیر فایل عکس را دریافت کنید و به اینستاگرام ارسال کنید
    photo_path = 'path_to_your_image.jpg'
    send_instagram_story(photo_path)
    await update.message.reply("استوری به اینستاگرام ارسال شد!")

# راه‌اندازی ربات تلگرام
async def main():
    # ایجاد شیء Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_story", send_story))

    # شروع ربات
    await application.run_polling()

# اجرای برنامه
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
