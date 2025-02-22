from app import app, db
from models import Task
from ai_helper import ask_ai  # استدعاء الذكاء الاصطناعي

# تشغيل التطبيق داخل الـ context الخاص به
with app.app_context():
    # استقبال بيانات المهمة من المستخدم
    title = input("📌 Enter the task title: ")
    description = input("📝 Enter task description: ")
    status = input("✅ Enter task status (pending, in_progress, done): ")



    priority = input("⚡ Enter task priority (high, medium, low): ").strip().lower()

    # استقبال وقت البداية والنهاية
    start_time = input("⏰ Enter start time (YYYY-MM-DD HH:MM): ")
    end_time = input("⏳ Enter end time (YYYY-MM-DD HH:MM): ")

    # التحقق من صحة الإدخالات
    valid_statuses = ["pending", "in_progress", "done"]
    valid_priorities = ["high", "medium", "low"]

    if status not in valid_statuses:
        print("⚠️ Error: Status must be 'pending', 'in_progress', or 'done'.")
    elif priority not in valid_priorities:
        print("⚠️ Error: Priority must be 'high', 'medium', or 'low'.")
    else:
        # إنشاء كائن المهمة
        new_task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            start_time=start_time,
            end_time=end_time
        )

        # إضافة المهمة إلى قاعدة البيانات
        db.session.add(new_task)
        db.session.commit()

        # توليد رد تفاعلي باستخدام الذكاء الاصطناعي
        ai_prompt = f"""
        You are a smart assistant that helps users manage their tasks. 
        A new task has been added with the following details:
        - Title: {title}
        - Description: {description}
        - Status: {status}
        - Priority: {priority}
        - Start Time: {start_time}
        - End Time: {end_time}
        
        Generate an engaging and positive response to acknowledge this task.
        """
        ai_response = ask_ai(ai_prompt)

        print(ai_response)  # طباعة الرد التفاعلي من الذكاء الاصطناعي