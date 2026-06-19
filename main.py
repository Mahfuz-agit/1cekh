import os
import time
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# ১. ব্যালেন্সড কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def process_video(video_id):
    try:
        # ট্রান্সক্রিপ্ট নেওয়া এবং ছোট করা (limit: 8000 tokens)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript])
        
        # জেমিনিকে ব্যালেন্সড প্রম্পট দেওয়া
        response = model.generate_content(f"Summarize this lecture briefly: {text[:8000]}")
        
        # সেভ করা
        with open(f"content/node_{video_id}.md", "w", encoding="utf-8") as f:
            f.write(f"# {video_id}\n\n{response.text}")
        
        print(f"Success: {video_id}")
        return True
    except Exception as e:
        print(f"Error for {video_id}: {e}")
        return False

# ২. সারাদিন কাজ করানোর জন্য লুপ (ব্যালেন্সড টাইম গ্যাপ)
videos = ["jNQXAC9IVRw", "ANOTHER_ID_HERE"] # ভিডিও আইডি লিস্ট

for vid in videos:
    success = process_video(vid)
    if success:
        time.sleep(60) # প্রতিটা রিকোয়েস্টের মাঝে ১ মিনিটের বিরতি (এরর এড়ানোর জন্য)
    else:
        time.sleep(300) # ফেইল করলে ৫ মিনিট পর আবার চেষ্টা করবে
