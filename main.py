import os
import sys
import json
import subprocess
import google.generativeai as genai

# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

videos_to_process = ["dQw4w9WgXcQ"] 

def curate_video(video_id):
    try:
        filename = f"content/node_{video_id}.md"
        if os.path.exists(filename):
            print(f"Skipping: {video_id} already exists.")
            return False

        # ১. ট্রান্সক্রিপ্ট নেওয়ার বুলেটপ্রুফ পদ্ধতি (Subprocess CLI)
        print(f"Fetching transcript for {video_id}...")
        result = subprocess.run(
            [sys.executable, '-m', 'youtube_transcript_api', video_id, '--format', 'json'],
            capture_output=True, text=True, check=True
        )
        
        transcript_data = json.loads(result.stdout)
        text = " ".join([item['text'] for item in transcript_data])
        
        # ২. সামারি তৈরি
        print("Generating AI Summary...")
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
        
    except subprocess.CalledProcessError as e:
        print(f"TRANSCRIPT ERROR: Could not fetch transcript. Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return False

for vid in videos_to_process:
    curate_video(vid)
