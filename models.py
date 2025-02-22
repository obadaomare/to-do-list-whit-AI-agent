from database import db

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}  # لضمان تحديث الجدول إذا كان موجوداً مسبقاً
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    priority = db.Column(db.String(20), nullable=False, default="medium")  # ✅ الأولوية كنص (high, medium, low)
    start_time = db.Column(db.String(50), nullable=True)
    end_time = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Task {self.title}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,  # ✅ ستظهر كـ "high", "medium", "low"
            "start_time": self.start_time,
            "end_time": self.end_time
        }
