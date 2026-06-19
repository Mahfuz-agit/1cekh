import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# API কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    # ইউটিউব আইডি
    video_id = "jNQXAC9IVRw"
    
    # ট্রান্সক্রিপ্ট সংগ্রহ
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([i['text'] for i in transcript])
    
    # জেমিনি দিয়ে প্রসেসিং
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze this lecture and provide:
    1. Concise Summary.
    2. Key Takeaways in bullet points.
    3. A brief 'Knowledge Graph' of core concepts.
    
    Content: {text[:8000]}
    """
    response = model.generate_content(prompt)
    
    # ফাইল সেভ
    with open(f"node_{video_id}.md", "w", encoding="utf-8") as f:
        f.write(f"# Knowledge Node: {video_id}\n\n{response.text}")
    print("Success: Node created.")

except Exception as e:
    print(f"Error: {str(e)}")
