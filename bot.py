from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import filters
from instabot import Bot  # کتابخانه اینستاگرام برای ارسال استوری

# توکن ربات تلگرام
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
INSTAGRAM_USERNAME = "YOUR_INSTAGRAM_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_INSTAGRAM_PASSWORD"

# راه‌اندازی ربات تلگرام
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# راه‌اندازی ربات اینستاگرام
instagram_bot = Bot()
instagram_bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

# دستور برای شروع کار ربات تلگرام
def start(update, context):
    update.message.reply_text('سلام! من ربات شما هستم.')

# دستورات ربات تلگرام
dispatcher.add_handler(CommandHandler("start", start))

# تابع برای ارسال استوری به اینستاگرام
def send_instagram_story(photo_path):
    instagram_bot.upload_story_photo(photo_path)

# تابع برای اکو کردن پیام‌های دریافتی
def echo(update, context):
    update.message.reply_text(update.message.text)

# وقتی عکس ارسال می‌شود، آن را ذخیره کرده و به اینستاگرام ارسال می‌کنیم
def handle_photo(update, context):
    file = update.message.photo[-1].get_file()  # گرفتن بزرگترین اندازه عکس
    file.download('photo.jpg')  # دانلود عکس به صورت محلی
    send_instagram_story('photo.jpg')  # ارسال عکس به استوری اینستاگرام

# تنظیم هندلر برای عکس‌های ارسالی
dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# MessageHandler برای فیلتر کردن پیام‌های متنی (غیر دستوری)
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# راه‌اندازی ربات تلگرام
updater.start_polling()

# ربات در حالت idle می‌ماند تا زمانی که متوقف شود
updater.idle()
