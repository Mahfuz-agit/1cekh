import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# জেমিনির চাবি সেট করা হচ্ছে
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# আপাতত একটি ছোট ভিডিও দিয়ে টেস্ট করছি
TARGET_VIDEO_ID = "dQw4w9WgXcQ" 

print("১. ভিডিওর ডেটা সংগ্রহ করা হচ্ছে...")
try:
    transcript = YouTubeTranscriptApi.get_transcript(TARGET_VIDEO_ID)
    raw_text = " ".join([item['text'] for item in transcript])
    
    print("২. জেমিনির ব্রেইনে পাঠানো হচ্ছে...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"এই ভিডিও ট্রান্সক্রিপ্টটির ৩ লাইনের একটি স্মার্ট সামারি দাও: {raw_text}")
    
    print("\n--- 🎯 এলিট রেজাল্ট ---")
    print(response.text)

except Exception as e:
    print(f"কোনো সমস্যা হয়েছে: {e}")
