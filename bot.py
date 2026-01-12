import telebot
import logging
import schedule
import time
import threading
from flask import Flask
from threading import Thread

# ২৪ ঘণ্টা সচল রাখার সার্ভার
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

logging.basicConfig(level=logging.INFO)
TOKEN = '8387682605:AAElAKcUHVl8kVz9eZxkBCbKtfrFHYFXMJ4'
bot = telebot.TeleBot(TOKEN)
MY_OWN_ID = 8233872409             
GROUP_CHAT_ID = -1003370221660     

def is_authorized(message):
    try:
        if (message.sender_chat and message.sender_chat.type == 'channel') or (message.forward_from_chat and message.forward_from_chat.type == 'channel'): return True
        user_id = message.from_user.id
        if user_id == MY_OWN_ID: return True
        status = bot.get_chat_member(message.chat.id, user_id).status
        return status in ['administrator', 'creator']
    except: return False

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        welcome_text = f"🎉 **স্বাগতম {member.first_name}!**\n━━━━━━━━━━━━━━━━━\n🛡️ নিরাপদ থাকতে অ্যাডমিনের অনুমতি ছাড়া লেনদেন করবেন না।"
        try: bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")
        except: pass

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if not message.text or is_authorized(message): return
    text = message.text.lower()
    if "http" in text or "www" in text:
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
    if "inbox" in text or "ইনবক্স" in text:
        warning = "⚠️ **সতর্কতা বার্তা** ⚠️\n━━━━━━━━━━━━━━\nগ্রুপে কোনো প্রকার লেনদেন করলে অবশ্যই **অ্যাডমিনের** অনুমতি নিয়ে করবেন।\n🚫 **ইনবক্সে গিয়ে লেনদেন করে প্রতারিত হলে এই গ্রুপ কর্তৃপক্ষ দায়ী থাকবে না।**"
        try: bot.reply_to(message, warning, parse_mode="Markdown")
        except: pass

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
