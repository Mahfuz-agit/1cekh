import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_video_notes(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript])
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Summarize this lecture and provide key takeaways and a knowledge graph: {text[:10000]}")
        return response.text
    except Exception as e:
        return f"Error: {e}"

# টেস্ট রান
video_id = "jNQXAC9IVRw"
content = get_video_notes(video_id)

with open(f"note_{video_id}.md", "w", encoding="utf-8") as f:
    f.write(f"# Knowledge Node: {video_id}\n\n{content}")
