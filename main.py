import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

videos_to_process = ["jNQXAC9IVRw"] 

def curate_video(video_id):
    try:
        # ১. ফাইলটি অলরেডি আছে কি না চেক করা (ডুপ্লিকেট এড়াতে)
        filename = f"content/node_{video_id}.md"
        if os.path.exists(filename):
            print(f"Skipping: {video_id} already exists.")
            return False

        # ২. ট্রান্সক্রিপ্ট নেওয়া
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript_list])
        
        # ৩. সামারি তৈরি
        prompt = f"Provide a high-quality, structured summary with key takeaways for the following content: {text[:8000]}"
        response = model.generate_content(prompt)

        # ৪. ফোল্ডার ও ফাইল সেভ
        if not os.path.exists("content"):
            os.makedirs("content")
    
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
        
        # ৫. ইনডেক্স আপডেট (যদি না থাকে)
        with open("content/index.md", "a", encoding="utf-8") as f:
            f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")
            
        print(f"Success: {video_id} curated.")
        return True
    except Exception as e:
        print(f"Error details: {e}")
        return False

for vid in videos_to_process:
    curate_video(vid)
