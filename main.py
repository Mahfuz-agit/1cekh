import os
import json
import subprocess
import google.generativeai as genai

# ১. এপিআই কি চেক
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL: GEMINI_API_KEY is missing!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

video_id = "dQw4w9WgXcQ" 
print(f"Starting pipeline for video: {video_id}")

# ২. পাইথনের বাইরে সরাসরি টার্মিনাল কমান্ড দিয়ে ট্রান্সক্রিপ্ট নামানো
print("Fetching transcript via CLI subprocess...")
temp_file = "transcript.json"

# টার্মিনালে সরাসরি রান করানো হচ্ছে: youtube_transcript_api video_id --format json
subprocess.run(
    ["youtube_transcript_api", video_id, "--format", "json", "--output", temp_file],
    check=True
)

# ৩. নামানো ফাইলটি পাইথন দিয়ে রিড করা
if not os.path.exists(temp_file):
    raise FileNotFoundError("CLI failed to create transcript file!")

with open(temp_file, "r", encoding="utf-8") as f:
    transcript_data = json.load(f)

text = " ".join([item['text'] for item in transcript_data])
print("Successfully loaded transcript text from CLI!")

# ৪. জেমিনি এপিআই কল
print("Sending data to Gemini API...")
prompt = f"Provide a high-quality, structured summary with key takeaways for the following content: {text[:4000]}"
response = model.generate_content(prompt)
print("Gemini successfully generated content!")

# ৫. ফোল্ডার ও ফাইল তৈরি
if not os.path.exists("content"):
    os.makedirs("content")

filename = f"content/node_{video_id}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")

with open("content/index.md", "a", encoding="utf-8") as f:
    f.write(f"\n* [Node: {video_id}](node_{video_id}.md)")

# অস্থায়ী ফাইলটি মুছে ফেলা
if os.path.exists(temp_file):
    os.remove(temp_file)

print(f"SUCCESS: File created successfully at {filename}")
