import os

# ১. content ফোল্ডার এবং index.md ফাইল তৈরি
os.makedirs("content", exist_ok=True)
with open("content/index.md", "w", encoding="utf-8") as f:
    f.write("# 🌌 Elite Knowledge Hub\n\nস্বাগতম আপনার পার্সোনাল নলেজ ইঞ্জিনে।")

# ২. index.html (ওয়েবসাইট ইন্টারফেস) তৈরি
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Elite Knowledge Hub</title>
    <style>
        body { margin: 0; background-color: #0b0f19; color: #f3f4f6; font-family: sans-serif; display: flex; height: 100vh; }
        .sidebar { width: 250px; background-color: #111827; padding: 20px; border-right: 1px solid #1f2937; }
        .main { flex: 1; display: flex; justify-content: center; align-items: center; background: radial-gradient(circle, #1e293b, #0b0f19); }
    </style>
</head>
<body>
    <div class="sidebar"><h2>🌌 Knowledge Hub</h2><hr><a href="#" style="color:#3b82f6; text-decoration:none;">🔗 Home</a></div>
    <div class="main"><div style="border:2px dashed #3b82f6; padding:30px; border-radius:50%;"><h3>Universe of Nodes</h3><p>● index.md</p></div></div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# ৩. গিটহাবে অটোমেটিক সেভ (Push) করার কমান্ড
os.system('git config --global user.name "GitHub Action"')
os.system('git config --global user.email "action@github.com"')
os.system('git add index.html content/')
os.system('git commit -m "Web interface files created"')
os.system('git push')
print("✅ সব ফাইল তৈরি এবং গিটহাবে সেভ হয়েছে!")
