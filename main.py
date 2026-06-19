import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

videos_to_process = ["jNQXAC9IVRw"] 

def curate_video(video_id):
    try:
        filename = f"content/node_{video_id}.md"
        if os.path.exists(filename):
            print(f"Skipping: {video_id} already exists.")
            return False

        # ১. ট্রান্সক্রিপ্ট নেওয়া
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript_list])
        
        # ২. সামারি তৈরি
        prompt = f"Provide a high-quality, structured summary with key takeaways for the following content: {text[:8000]}"
        response = model.generate_content(prompt)

        # ৩. ফোল্ডার ও ফাইল সেভ
        if not os.path.exists("content"):
            os.makedirs("content")
    
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
        
        # ৪. ইনডেক্স আপডেট
        with open("content/index.md", "a", encoding="utf-8") as f:
            f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")
            
        print(f"Success: {video_id} curated and saved at {filename}")
        return True
        
    except Exception as e:
        print(f"ERROR DETAILS: {e}")
        # লাইব্রেরির কোথায় সমস্যা তা বের করার জন্য ডিবাগিং
        import youtube_transcript_api
        print(f"DEBUGGING MODULE PATH: {youtube_transcript_api.__file__}")
        return False

for vid in videos_to_process:
    curate_video(vid)
