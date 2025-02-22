from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from database import db
from models import Task
from ai_helper import determine_priority , ask_ai , generate_task_response
from google_calendar import add_event_to_google_calendar

app = Flask(__name__)
CORS(app)  # السماح للواجهة الأمامية بالاتصال بالـ API

# تكوين قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات مع التطبيق
with app.app_context():
    db.init_app(app)
    db.create_all()

# الصفحة الرئيسية: عرض جميع المهام
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# عرض جدول المهام (واجهة منفصلة)
@app.route('/tasks/view', methods=['GET'])
def view_tasks():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)

# API: جلب جميع المهام بصيغة JSON
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# API: إضافة مهمة جديدة مع نظام الجدولة وتحديد الأولوية
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "A title for the task must be provided."}), 400

    title = data['title']
    description = data.get('description', '')
    start_time = data.get('start_time', 'No deadline specified')
    end_time = data.get('end_time', '')
    
    # تحديد الأولوية باستخدام الذكاء الاصطناعي بناءً على الوصف
    priority = determine_priority(description)

    # إنشاء المهمة وإضافتها إلى قاعدة البيانات
    new_task = Task(title=title, description=description, priority=priority,
                    start_time=start_time, end_time=end_time)
    db.session.add(new_task)
    db.session.commit()

    # حساب عدد المهام المتبقية
    task_count = Task.query.count()

    # توليد رد تفاعلي ديناميكي
    response_message = generate_task_response(title, start_time, priority, task_count)


 # ✅ إضافة المهمة إلى تقويم Google
    if start_time != "No deadline specified" and end_time:
        add_event_to_google_calendar(title, description, start_time, end_time)


    return jsonify({"message": response_message, "task": new_task.to_dict()}), 201

# API: تحديث مهمة
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'priority' in data:
        task.priority = data['priority']
    if 'start_time' in data:
        task.start_time = data['start_time']
    if 'end_time' in data:
        task.end_time = data['end_time']
    
    db.session.commit()
    return jsonify(task.to_dict())

# API: حذف مهمة
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "The task was successfully deleted."})

# API: نقطة نهاية للدردشة مع الذكاء الاصطناعي
@app.route("/ask-ai", methods=["POST"])
def chat_with_ai():
    data = request.json
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"error": "The message cannot be empty"}), 400

    response = ask_ai(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
