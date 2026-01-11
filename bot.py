import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# আপনার বটের তথ্য
TOKEN = '8387682605:AAElAKcUHVl8kVz9eZxkBCbKtfrFHYFXMJ4'
GROUP_ID = -1002347318556 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    
    # লিঙ্ক ডিলিট করার ফাংশন
    if "http" in text or "www" in text:
        try:
            await update.message.delete()
            return
        except:
            pass

    # কিওয়ার্ড রিপ্লাই
    keywords = ["inbox", "ইনবক্স", "লেনদেন"]
    if any(word in text for word in keywords):
        await update.message.reply_text("📢 সতর্কতা: লেনদেন করলে এডমিনের সাথে করবেন। ইনবক্সে গিয়ে লেনদেন করে প্রতারিত হলে এই গ্রুপ কর্তৃপক্ষ দায়ী থাকবে না।")

def main():
    # রেন্ডারের জন্য পোর্ট সেটিং
    port = int(os.environ.get("PORT", 10000))
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    # পোলিং মোডে চালানো
    application.run_polling()

if __name__ == '__main__':
    main()
