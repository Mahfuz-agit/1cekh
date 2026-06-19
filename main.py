import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# যে ভিডিওগুলো আপনি প্রসেস করতে চান তার আইডি এখানে দিন
videos_to_process = ["jNQXAC9IVRw"] 

def curate_video(video_id):
    try:
        # ১. ট্রান্সক্রিপ্ট সংগ্রহ
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript])
        
        # ২. Strict Rule দিয়ে যাচাই ও সামারি তৈরি
        prompt = f"""
        Strict Rule: Analyze this video content. 
        Is this educational and high-quality for a 'Knowledge Hub'? 
        If YES, provide a structured summary with key takeaways and a knowledge graph.
        If NO (it's clickbait, entertainment, or irrelevant), return only the word "REJECT".
        
        Content: {text[:8000]}
        """
        response = model.generate_content(prompt)
        
        # ৩. ফিল্টারিং লজিক
        if "REJECT" in response.text.upper():
            print(f"Skipping: {video_id} (Irrelevant)")
            return False
            
        # ৪. নোট সেভ করা
        filename = f"content/node_{video_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
        
        # ৫. ইনডেক্স আপডেট করা
        with open("content/index.md", "a", encoding="utf-8") as f:
            f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")
            
        print(f"Success: {video_id} curated.")
        return True
    except Exception as e:
        print(f"Error for {video_id}: {e}")
        return False

# ভিডিওগুলো লুপে চালানো
for vid in videos_to_process:
    curate_video(vid)
