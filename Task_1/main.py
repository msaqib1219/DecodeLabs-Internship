import json

TASKS_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from a JSON file."""
    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
            # Data Migration: Convert legacy strings to dictionary objects
            normalized_tasks = []
            for item in data:
                if isinstance(item, str):
                    normalized_tasks.append({"title": item, "completed": False})
                else:
                    normalized_tasks.append(item)
            # Self-healing: Update the file immediately if migration occurred
            if normalized_tasks != data:
                save_tasks(normalized_tasks)
            return normalized_tasks
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        # If the file is corrupted or empty, return an empty list and print a warning
        print(f"Warning: Could not decode tasks from {TASKS_FILE}. Starting with an empty list.")
        return []

def save_tasks(tasks):
    """Saves tasks to a JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4) # Use indent for pretty-printing

def main():
    my_tasks = load_tasks()  # Load tasks at the start of the application
    print("Hello from your To-Do List Application!")

    while True:
        print("\n--- Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Mark Task Completed")
        print("5. Save and Quit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            # Input: Get the new task description
            new_task = input("Enter the task description: ").strip()
            # Process: Store task as a dictionary object for metadata support
            task_item = {"title": new_task, "completed": False}
            my_tasks.append(task_item)
            save_tasks(my_tasks)
            # Output: Confirmation message
            print(f"'{new_task}' has been added to your list.")
        elif choice == '2':
            # Output: Display all tasks
            if not my_tasks:
                print("Your To-Do list is empty!")
            else:
                print("\n--- Your Tasks ---")
                # Iterator Protocol: Loop through the list to display items
                for index, task in enumerate(my_tasks, 1):
                    status = "[X]" if task.get("completed") else "[ ]"
                    print(f"{index}. {status} {task['title']}")
        elif choice == '3':
            if not my_tasks:
                print("Nothing to delete.")
            else:
                try:
                    task_num = int(input(f"Enter task number (1-{len(my_tasks)}) to delete: "))
                    if 1 <= task_num <= len(my_tasks):
                        removed_task = my_tasks.pop(task_num - 1)
                        save_tasks(my_tasks)
                        print(f"Deleted: {removed_task['title']}")
                    else:
                        print("Error: Task number out of range.")
                except ValueError:
                    print("Error: Please enter a valid numerical ID.")

        elif choice == '4':
            if not my_tasks:
                print("No tasks to modify.")
            else:
                try:
                    task_num = int(input(f"Enter task number (1-{len(my_tasks)}) to mark as complete: "))
                    if 1 <= task_num <= len(my_tasks):
                        # State Mutation
                        my_tasks[task_num - 1]['completed'] = True
                        save_tasks(my_tasks)
                        print(f"Status updated for: {my_tasks[task_num - 1]['title']}")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Error: Please enter a number.")

        elif choice == '5':
            print("Session ended.")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
