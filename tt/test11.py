tasks = []

def add_task():
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (низкий / средний / высокий): ").lower()

    task = {
        "title": title,
        "priority": priority,
        "status": "в процессе"
    }

    tasks.append(task)
    print("Задача успешно добавлена!\n")

def show_all_tasks():
    if not tasks:
        print("Задач нет.\n")
        return

    print("\n--- Список всех задач ---")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} | Приоритет: {task['priority']} | Статус: {task['status']}")
    print()

def complete_task():
    name = input("Введите название задачи, которую хотите отметить выполненной: ")

    for task in tasks:
        if task["title"] == name:
            task["status"] = "выполнено"
            print("Задача отмечена как выполненная!\n")
            return

    print("Такой задачи нет.\n")


def show_by_priority():
    priority = input("Введите приоритет (низкий / средний / высокий): ").lower()

    found = False
    print(f"\n--- Задачи с приоритетом '{priority}' ---")

    for task in tasks:
        if task["priority"] == priority:
            print(f"- {task['title']} | Статус: {task['status']}")
            found = True

    if not found:
        print("Задач с таким приоритетом нет.")

    print()

def delete_task():
    name = input("Введите название задачи, которую хотите удалить: ")

    for task in tasks:
        if task["title"] == name:
            tasks.remove(task)
            print("Задача успешно удалена!\n")
            return

    print("Такой задачи нет.\n")


while True:
    print("Выберите действие:")
    print("1 — Добавить задачу")
    print("2 — Показать все задачи")
    print("3 — Отметить задачу выполненной")
    print("4 — Показать задачи по приоритету")
    print("5 — Удалить задачу")
    print("0 — Выход")

    choice = input("Ваш выбор: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        show_all_tasks()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        show_by_priority()
    elif choice == "5":
        delete_task()
    elif choice == "0":
        print("Выход из программы. До свидания!")
        break
    else:
        print("Неизвестная команда, попробуйте снова.\n")