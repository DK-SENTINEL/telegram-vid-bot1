import os
import telebot
from yt_dlp import YoutubeDL

# তোমার বটের টোকেন
API_TOKEN = '8415339905:AAH1xenmzsyHBxULUVpAG1Vmnv7aNw8woyw'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    # সমর্থিত প্ল্যাটফর্ম
    platforms = ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "tiktok.com"]
    
    if any(platform in url for platform in platforms):
        bot.reply_to(message, "ভিডিওটি বিশ্লেষণ করা হচ্ছে... ⏳")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'playlist_items': '1-10', # সর্বোচ্চ ১০টি ভিডিও
                'quiet': True,
                'no_warnings': True
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if 'entries' in info:
                    videos = info['entries']
                    bot.reply_to(message, f"প্লেলিস্ট পাওয়া গেছে! প্রথম {len(videos)}টি ভিডিও প্রসেস হচ্ছে... 📚")
                else:
                    videos = [info]

                for index, video in enumerate(videos):
                    if len(videos) > 1:
                        bot.send_message(message.chat.id, f"ভিডিও {index+1}/{len(videos)} আপলোড হচ্ছে... 📤")
                    
                    file_name = ydl.prepare_filename(video)
                    title = video.get('title', 'Video')
                    
                    # স্পেশাল ক্যারেক্টার ক্লিন করা
                    safe_title = title.replace('_', ' ').replace('*', ' ').replace('[', ' ').replace(']', ' ')
                    caption_text = f"🎬 Title: {safe_title}\n\n📥 Downloaded by: @cyber24_uca_offcial  This Bot Admin @ucasentinel"
                    
                    if os.path.exists(file_name):
                        with open(file_name, 'rb') as v:
                            bot.send_video(message.chat.id, v, caption=caption_text)
                        os.remove(file_name)

        except Exception as e:
            bot.reply_to(message, f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

# ইন্টারনেট কানেকশন এরর দিলেও বট যেন বন্ধ না হয় (Retry logic)
bot.infinity_polling(timeout=10, long_polling_timeout=5)
