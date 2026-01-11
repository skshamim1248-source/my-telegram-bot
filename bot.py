import logging
import re
import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# আপনার বটের তথ্য
TOKEN = '8387682605:AAElAKcUHVl8kVz9eZxkBCbKtfrFHYFXMJ4'
GROUP_ID = -1002347318556 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# প্রতিদিন সকাল ৮টায় গুড মর্নিং ফাংশন
async def send_good_morning(context: ContextTypes.DEFAULT_TYPE):
    text = "☀️ শুভ সকাল! \nআপনার আজকের দিনটি ভালো কাটুক। আমাদের গ্রুপে সক্রিয় থাকার জন্য ধন্যবাদ! 😊"
    await context.bot.send_message(chat_id=GROUP_ID, text=text)

# নতুন মেম্বার আসলে স্বাগতম মেসেজ
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name
        group = update.effective_chat.title
        text = f"আসসালামু আলাইকুম {name}!\nআমাদের {group} গ্রুপে আপনাকে স্বাগতম! 😊"
        await update.message.reply_text(text)

# লিঙ্ক ডিলিট এবং ইনবক্স সতর্কবার্তা
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    message_text = update.message.text.lower()
    user_name = update.message.from_user.first_name

    # লিঙ্ক ডিটেকশন ও ডিলিট
    urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+)', message_text)
    if urls:
        try:
            await update.message.delete()
            await update.message.reply_text(f"⚠️ {user_name}, লিঙ্ক দেওয়া নিষেধ! পরবর্তীতে দিলে রিমুভ করা হবে।")
        except: pass
        return

    # ইনবক্স এবং লেনদেন সতর্কবার্তা
    inbox_keywords = ['inbox', 'ইনবক্স', 'ইনবক্সে আসেন', 'লেনদেন']
    if any(keyword in message_text for keyword in inbox_keywords):
        warning_text = (
            "📢 **সতর্কবার্তা:**\n"
            "লেনদেন করলে এডমিনের সাথে করবেন। ইনবক্সে গিয়ে লেনদেন করে প্রতারিত হলে এই গ্রুপ কর্তৃপক্ষ দায়ী থাকবে না।"
        )
        await update.message.reply_text(warning_text, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    job_queue = app.job_queue
    # সময় সেট করা (সকাল ৮টা)
    job_queue.run_daily(send_good_morning, time=datetime.time(hour=8, minute=0, second=0))
