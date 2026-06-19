import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# জেমিনি এপিআই সেটআপ
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ভিডিও আইডি এবং ফাইল লোকেশন
video_id = "jNQXAC9IVRw"
file_path = f"content/node_{video_id}.md"

try:
    # ১. ইউটিউব থেকে ট্রান্সক্রিপ্ট নেওয়া
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([i['text'] for i in transcript])
    
    # ২. জেমিনি দিয়ে নোট তৈরি
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Summarize this lecture, give key takeaways, and a knowledge graph: {text[:8000]}"
    response = model.generate_content(prompt)
    
    # ৩. কন্টেন্ট ফোল্ডারে নোট সেভ করা
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
    
    # ৪. index.md এ লিংক যোগ করা (যদি আগে না থাকে)
    new_link = f"\n* [Node: {video_id}](node_{video_id}.md)"
    with open("content/index.md", "a", encoding="utf-8") as f:
        f.write(new_link)

    print("Success: File created and Index updated.")

except Exception as e:
    print(f"Error: {e}")
