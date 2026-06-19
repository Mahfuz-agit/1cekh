import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

videos_to_process = ["jNQXAC9IVRw"] 

def curate_video(video_id):
    try:
        # সঠিক পদ্ধতিতে ট্রান্সক্রিপ্ট নেওয়া
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript_list])
        
        prompt = f"Summarize this: {text[:8000]}"
        response = model.generate_content(prompt)

        # ফোল্ডার চেক ও ফাইল সেভ নিশ্চিত করা
        if not os.path.exists("content"):
            os.makedirs("content")

    
        filename = f"content/node_{video_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
        
        with open("content/index.md", "a", encoding="utf-8") as f:
            f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")
            
        return True
    except Exception as e:
        print(f"Error details: {e}") # এররটি লগে ভালো করে দেখাবে
        return False

for vid in videos_to_process:
    curate_video(vid)
