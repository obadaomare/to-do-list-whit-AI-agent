def __repr__(self):
        return f'Task {self.title}'
def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }