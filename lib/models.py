class Task:
    def __init__(self, title, completed=False):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        self.title = title.strip()
        self.completed = completed

    def complete(self):
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }