import os


class TodoApp:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.txt"
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = [line.strip().split("|") for line in f.readlines()]

    def save_tasks(self):
        with open(self.filename, "w") as f:
            for task in self.tasks:
                f.write(f"{task[0]}|{task[1]}\n")

    def add_task(self, task):
        self.tasks.append([task, "Pending"])
        self.save_tasks()
        print(f"Task '{task}' added successfully.")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task[0]} - {task[1]}")

    def mark_complete(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            self.tasks[task_index - 1][1] = "Completed"
            self.save_tasks()
            print(f"Task '{self.tasks[task_index - 1][0]}' marked as completed.")
        else:
            print("Invalid task number.")

    def remove_task(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            removed_task = self.tasks.pop(task_index - 1)
            self.save_tasks()
            print(f"Task '{removed_task[0]}' removed successfully.")
        else:
            print("Invalid task number.")


def main():
    app = TodoApp()

    while True:
        print("\n==== Todo App ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            task = input("Enter task description: ")
            app.add_task(task)
        elif choice == "2":
            app.view_tasks()
        elif choice == "3":
            app.view_tasks()
            task_index = int(input("Enter the task number to mark as complete: "))
            app.mark_complete(task_index)
        elif choice == "4":
            app.view_tasks()
            task_index = int(input("Enter the task number to remove: "))
            app.remove_task(task_index)
        elif choice == "5":
            print("Thank you for using the Todo App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
