import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# قراءة مفتاح Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# التأكد من أن المفتاح تم تحميله بشكل صحيح
if not GEMINI_API_KEY:
    raise ValueError("⚠️ لم يتم العثور على مفتاح Gemini API، تأكد من إضافته إلى ملف .env")
