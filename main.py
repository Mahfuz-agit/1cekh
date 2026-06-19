import os
import json
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# ১. এপিআই কি চেক (যদি কি না থাকে তবে এখানেই কোড ক্র্যাশ করবে)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL: GEMINI_API_KEY is completely missing in GitHub Secrets!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# টেস্ট করার জন্য একটি নিশ্চিত সচল ভিডিও আইডি
video_id = "dQw4w9WgXcQ" 

print(f"Starting pipeline for video: {video_id}")

# ২. ট্রান্সক্রিপ্ট আনা (সমস্যা হলে গিটহাব অ্যাকশন এখানেই ফেইল করবে)
print("Attempting to fetch YouTube transcript...")
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
text = " ".join([i['text'] for i in transcript_list])
print("Successfully fetched transcript!")

# ৩. জেমিনি এপিআই কল (এপিআই কি নষ্ট বা কোটা শেষ হলে এখানে ক্র্যাশ করবে)
print("Sending data to Gemini API...")
prompt = f"Provide a high-quality, structured summary with key takeaways for the following content: {text[:4000]}"
response = model.generate_content(prompt)
print("Gemini successfully generated content!")

# ৪. ফাইল ও ফোল্ডার তৈরি
if not os.path.exists("content"):
    os.makedirs("content")

filename = f"content/node_{video_id}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")

with open("content/index.md", "a", encoding="utf-8") as f:
    f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")

print(f"SUCCESS: File created at {filename}")
