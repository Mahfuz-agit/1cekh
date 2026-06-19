import os
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# কনফিগারেশন
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def get_video_notes(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript])
        
        prompt = f"Provide a concise summary, key takeaways, and a knowledge graph of related resources for this lecture: {text[:15000]}"
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# টেস্ট ভিডিও আইডি (উদাহরণ)
video_id = "jNQXAC9IVRw" 
content = get_video_notes(video_id)

with open(f"note_{video_id}.md", "w", encoding="utf-8") as f:
    f.write(f"# Knowledge Node: {video_id}\n\n{content}")
