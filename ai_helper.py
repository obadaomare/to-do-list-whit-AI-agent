import google.generativeai as genai
from config import GEMINI_API_KEY
import time

# تهيئة API
if not GEMINI_API_KEY:
    raise ValueError("❌ API key not found! Make sure GEMINI_API_KEY is set in config.py")

genai.configure(api_key=GEMINI_API_KEY)

def ask_ai(user_input, max_retries=3, wait_time=5):
    """ يرسل استفسارًا إلى Gemini API ويحاول إعادة المحاولة عند الفشل """
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_input)

            if hasattr(response, "text") and response.text:
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                return response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else "❌ No response received."
            else:
                return "❌ Unexpected or empty response."
        
        except Exception as e:
            print(f"⚠️ Error connecting to Gemini API (Attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # انتظر قليلاً قبل إعادة المحاولة
            else:
                print("❌ AI response unavailable. Continuing without AI feedback.")
                return "✅ Task added successfully, but AI response is unavailable."

def determine_priority(task_description):
    """ يستخدم الذكاء الاصطناعي لتحديد أولوية المهمة بناءً على وصفها """
    try:
        prompt = f"Based on the following task description, set its priority between (High, Medium, Low):\n\n{task_description}\n\nPriority:"
        response = ask_ai(prompt)
        priority = response.strip().lower()
        return priority if priority in ["high", "medium", "low"] else "medium"
    except Exception as e:
        print(f"⚠️ Error determining priority: {e}")
        return "medium"  # الافتراضي في حالة الخطأ

def generate_task_response(title, start_time, end_time, priority):
    """ ينشئ ردًا تفاعليًا عند إضافة مهمة جديدة باستخدام الذكاء الاصطناعي """
    try:
        prompt = (
            f"I have added a new task titled '{title}', scheduled to start at {start_time} and end at {end_time}. "
            f"The assigned priority is {priority}. Can you confirm this in a friendly and engaging way?"
        )
        ai_response = ask_ai(prompt)
        if ai_response == "✅ Task added successfully, but AI response is unavailable.":
            return f"Task '{title}' added successfully! 📆 Starts at: {start_time}, Ends at: {end_time} ✅ Priority: {priority}"
        return ai_response
    except Exception as e:
        print(f"⚠️ Error generating AI response: {e}")
        return f"Task '{title}' added successfully! 📆 Starts at: {start_time}, Ends at: {end_time} ✅ Priority: {priority}"

# ✅ اختبار سريع
if __name__ == "__main__":
    print(ask_ai("Where is Syria?"))
    print(determine_priority("This task needs to be done very urgently because it affects customers."))
    print(generate_task_response("Buy groceries", "2025-03-01 10:00", "2025-03-01 12:00", "High"))
