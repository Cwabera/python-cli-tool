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


class User:
    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("User name cannot be empty")

        self.name = name.strip()
        self.tasks = []

    def add_task(self, task):
        if not isinstance(task, Task):
            raise ValueError("task must be a Task object")

        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def get_task_by_title(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }