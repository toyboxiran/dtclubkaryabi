from instagrapi import Client
from telegram import Update
from telegram.ext import Application, CommandHandler

# اطلاعات مورد نیاز
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
INSTAGRAM_USERNAME = 'YOUR_INSTAGRAM_USERNAME'
INSTAGRAM_PASSWORD = 'YOUR_INSTAGRAM_PASSWORD'

# راه‌اندازی کلاینت اینستاگرام
instagram_client = Client()

# تغییر User-Agent برای جلوگیری از محدودیت‌های اینستاگرام
instagram_client.set_user_agent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# ورود به اینستاگرام
try:
    instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    print("Login to Instagram successful!")
except Exception as e:
    print(f"Error logging into Instagram: {e}")

# تابع استارت ربات تلگرام
async def start(update: Update, context):
    await update.message.reply_text("سلام! ربات آماده است.")

# تابع ارسال استوری به اینستاگرام
async def send_story(update: Update, context):
    photo_path = 'path_to_your_image.jpg'  # مسیر عکس
    try:
        instagram_client.photo_upload(photo_path, caption="استوری جدید از ربات!")
        await update.message.reply_text("استوری با موفقیت ارسال شد!")
    except Exception as e:
        await update.message.reply_text(f"خطا در ارسال استوری: {e}")

# تنظیمات ربات تلگرام
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # اضافه کردن دستورها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_story", send_story))

    # اجرا
    application.run_polling()

if __name__ == "__main__":
    main()
