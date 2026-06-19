import os
from google import genai

# গুগলের একদম লেটেস্ট ২০২৬ স্ট্যান্ডার্ড অনুযায়ী ক্লায়েন্ট সেটআপ
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("১. সিস্টেম কানেক্ট হচ্ছে...")
try:
    print("২. জেমিনির ব্রেইনে মেসেজ পাঠানো হচ্ছে...")
    # একদম নতুন ও স্ট্যাবল জেমিনি মডেল ব্যবহার করা হচ্ছে
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="আমাকে ৩ লাইনের একটি স্মার্ট ও পাওয়ারফুল মোটিভেশনাল কথা বলো।"
    )
    
    print("\n--- 🎯 এলিট রেজাল্ট ---")
    print(response.text)

except Exception as e:
    print(f"কোনো সমস্যা হয়েছে: {e}")
