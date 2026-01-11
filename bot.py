import os
import telebot

# আপনার বটের তথ্য
TOKEN = '8387682605:AAElAKcUHVl8kVz9eZxkBCbKtfrFHYFXMJ4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text.lower()
    
    # লিঙ্ক ডিলিট করা
    if "http" in text or "www" in text:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    # কিওয়ার্ড রিপ্লাই
    keywords = ["inbox", "ইনবক্স", "লেনদেন"]
    if any(word in text for word in keywords):
        bot.reply_to(message, "📢 সতর্কতা: লেনদেন করলে এডমিনের সাথে করবেন। ইনবক্সে গিয়ে লেনদেন করে প্রতারিত হলে এই গ্রুপ কর্তৃপক্ষ দায়ী থাকবে না।")

print("Bot is running...")
bot.infinity_polling()
