import json
import os
from datetime import datetime


class TodoTaskTool:
    def __init__(self, filename='tasks.json'):
        """
        Initialize the Todo Task Tool with a JSON file for persistent storage.

        Args:
            filename (str): Name of the file to store tasks (default: 'tasks.json')
        """
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from the JSON file. Create an empty list if file doesn't exist.

        Returns:
            list: List of tasks
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Error reading {self.filename}. Starting with an empty task list.")
            return []

    def save_tasks(self):
        """
        Save tasks to the JSON file.
        """
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError:
            print(f"Error saving tasks to {self.filename}")

    def add_task(self, description, priority='medium', due_date=None):
        """
        Add a new task to the task list.

        Args:
            description (str): Task description
            priority (str): Task priority (low/medium/high)
            due_date (str, optional): Due date in YYYY-MM-DD format

        Returns:
            dict: The newly created task
        """
        # Validate priority
        priority = priority.lower()
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'

        # Validate due date
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD. No due date set.")
                due_date = None

        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'priority': priority,
            'due_date': due_date,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.tasks.append(task)
        self.save_tasks()
        return task

    def list_tasks(self, filter_type=None):
        """
        List tasks with optional filtering.

        Args:
            filter_type (str, optional): Filter by 'completed' or 'pending'

        Returns:
            list: Filtered list of tasks
        """
        if filter_type == 'completed':
            return [task for task in self.tasks if task['completed']]
        elif filter_type == 'pending':
            return [task for task in self.tasks if not task['completed']]
        return self.tasks

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete.

        Args:
            task_id (int): ID of the task to mark complete

        Returns:
            bool: True if task was found and marked, False otherwise
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return True
        print(f"Task with ID {task_id} not found.")
        return False

    def remove_task(self, task_id):
        """
        Remove a task from the list.

        Args:
            task_id (int): ID of the task to remove

        Returns:
            bool: True if task was found and removed, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                # Reindex tasks
                for j, t in enumerate(self.tasks, 1):
                    t['id'] = j
                self.save_tasks()
                return True
        print(f"Task with ID {task_id} not found.")
        return False


def main():
    """
    Main interactive function to use the Todo Task Tool
    """
    todo = TodoTaskTool()

    while True:
        print("\n--- Todo Task Tool ---")
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. List Completed Tasks")
        print("4. List Pending Tasks")
        print("5. Mark Task Complete")
        print("6. Remove Task")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter priority (low/medium/high, default: medium): ") or 'medium'
            due_date = input("Enter due date (YYYY-MM-DD, optional): ") or None
            task = todo.add_task(description, priority, due_date)
            print(f"Task added with ID {task['id']}")

        elif choice == '2':
            tasks = todo.list_tasks()
            for task in tasks:
                status = "✓" if task['completed'] else " "
                print(f"ID: {task['id']} [{status}] {task['description']} "
                      f"(Priority: {task['priority']}, "
                      f"Due: {task['due_date'] or 'No due date'})")

        elif choice == '3':
            tasks = todo.list_tasks('completed')
            for task in tasks:
                print(f"ID: {task['id']} {task['description']} "
                      f"(Priority: {task['priority']})")

        elif choice == '4':
            tasks = todo.list_tasks('pending')
            for task in tasks:
                print(f"ID: {task['id']} {task['description']} "
                      f"(Priority: {task['priority']}, "
                      f"Due: {task['due_date'] or 'No due date'})")

        elif choice == '5':
            task_id = int(input("Enter task ID to mark complete: "))
            if todo.mark_task_complete(task_id):
                print("Task marked as complete.")

        elif choice == '6':
            task_id = int(input("Enter task ID to remove: "))
            if todo.remove_task(task_id):
                print("Task removed.")

        elif choice == '7':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()