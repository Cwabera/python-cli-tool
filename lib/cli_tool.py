import argparse
import json
from pathlib import Path

from lib.models import Task, User

DATA_FILE = Path(__file__).resolve().parent.parent / "tasks_data.json"


def load_users():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

    users = {}

    for username, user_data in data.items():
        user = User(user_data["name"])

        for task_data in user_data.get("tasks", []):
            task = Task(
                task_data["title"],
                completed=task_data.get("completed", False)
            )
            user.tasks.append(task)

        users[username] = user

    return users


def save_users(users):
    data = {}

    for username, user in users.items():
        data[username] = user.to_dict()

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


users = load_users()


def add_task(args):
    global users

    if args.user not in users:
        users[args.user] = User(args.user)

    task = Task(args.title)
    users[args.user].add_task(task)
    save_users(users)


def complete_task(args):
    global users

    user = users.get(args.user)

    if user is None:
        print(f"User '{args.user}' not found.")
        return

    task = user.get_task_by_title(args.title)

    if task is None:
        print(f"Task '{args.title}' not found for user '{args.user}'.")
        return

    task.complete()
    save_users(users)


def view_tasks(args):
    user = users.get(args.user)

    if user is None:
        print(f"User '{args.user}' not found.")
        return

    if not user.tasks:
        print(f"No tasks found for user '{args.user}'.")
        return

    print(f"Tasks for {user.name}:")
    for task in user.tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"- {task.title} [{status}]")


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    view_parser = subparsers.add_parser("view-tasks", help="View all tasks for a user")
    view_parser.add_argument("user")
    view_parser.set_defaults(func=view_tasks)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()