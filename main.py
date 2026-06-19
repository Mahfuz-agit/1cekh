import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# পরীক্ষা করার জন্য আইডি
video_id = "jNQXAC9IVRw"

def test_save():
    try:
        # ১. ট্রান্সক্রিপ্ট আনার চেষ্টা
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript_list])
        
        # ২. ফাইল পাথ সেট করা
        if not os.path.exists("content"):
            os.makedirs("content")
        
        filename = "content/test_file.md"
        
        # ৩. ফাইল তৈরি
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Test file content working!")
        
        print(f"DEBUG: File successfully created at {os.path.abspath(filename)}")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

test_save()
