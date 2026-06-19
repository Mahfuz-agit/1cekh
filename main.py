import os
import google.generativeai as genai

# জেমিনির চাবি সেট করা হচ্ছে
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

print("১. সিস্টেম কানেক্ট হচ্ছে...")
try:
    print("২. জেমিনির ব্রেইনে মেসেজ পাঠানো হচ্ছে...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("আমাকে ৩ লাইনের একটি স্মার্ট ও পাওয়ারফুল মোটিভেশনাল কথা বলো।")
    
    print("\n--- 🎯 এলিট রেজাল্ট ---")
    print(response.text)

except Exception as e:
    print(f"কোনো সমস্যা হয়েছে: {e}")
