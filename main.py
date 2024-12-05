from task_manager import TaskManager


def main():
    """Основной цикл программы для взаимодействия с пользователем"""
    manager = TaskManager()

    while True:
        print("\nМенеджер задач:")
        print("\t1. Просмотр задач")
        print("\t2. Добавить задачу")
        print("\t3. Изменение задач")
        print("\t4. Удаление задач")
        print("\t5. Поиск задач")
        print("\t6. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            """Просмотр задач"""
            while True:
                print("\nМенеджер задач:")
                print("\tПросмотр задач:")
                print("\t\t1. Просмотр всех задач")
                print("\t\t2. Просмотр задач по категориям")
                print("\t\t3. Назад")
                choice = input("Выберите опцию: ")
                if choice == '1':
                    """Просмотр всех задач"""
                    print("\nВсе задачи:")
                    manager.display_tasks(manager.tasks)
                elif choice == '2':
                    """Просмотр задач по категориям"""
                    print("\nЗадачи по категориям:")
                    manager.display_grouped_tasks()
                elif choice == '3':
                    """Выход из просмотра задач"""
                    print("\nНазад...")
                    break
                else:
                    print("\nНеверный выбор. Пожалуйста, попробуйте снова.")
        elif choice == '2':
            """Добавление новой задачи"""
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория задачи: ")
            due_date = input("Срок выполнения (dd.mm.yyyy): ")
            priority = input("Приоритет (Низкий, Средний, Высокий): ")
            manager.add_task(title, description, category, due_date, priority)
        elif choice == '3':
            """Редактирование существующей задачи"""
            while True:
                print("\nМенеджер задач:")
                print("\tИзменение задач:")
                print("\t\t1. Изменить параметры задачи")
                print("\t\t2. Изменить статус задачи")
                print("\t\t3. Назад")
                choice = input("Выберите опцию: ")
                if choice == '1' or choice == '2':
                    task_id = None
                    try:
                        task_id = int(input("ID задачи для изменения: "))
                    except ValueError:
                        print("Ошибка: Введено некорректное значение. "
                              "Пожалуйста, введите число.")
                        continue

                    tasks = manager.search_tasks(task_id)
                    if not tasks:
                        continue
                    print("\nЗадача, которую будем редактировать:")
                    manager.display_tasks(tasks)
                    if choice == '1':
                        """Изменить параметры задачи"""
                        title = input("Новое название задачи (оставьте "
                                      "пустым, если не нужно): ")
                        description = input("Новое описание задачи (оставьте "
                                            "пустым, если не нужно): ")
                        category = input("Новая категория задачи (оставьте "
                                         "пустым, если не нужно): ")
                        due_date = input("Новый срок выполнения (оставьте "
                                         "пустым, если не нужно): ")
                        priority = input("Новый приоритет (оставьте "
                                         "пустым, если не нужно): ")
                        manager.update_task(task_id, title, description,
                                            category, due_date, priority)
                    elif choice == '2':
                        """Изменить статус задачи"""
                        status = input("Новый статус (Выполнена/"
                                       "Не выполнена): ")
                        manager.update_task(task_id=task_id, status=status)
                elif choice == '3':
                    """Выход из изменения задачи"""
                    print("\nНазад...")
                    break
                else:
                    print("\nНеверный выбор. Пожалуйста, попробуйте снова.")
        elif choice == '4':
            """Удаление задач"""
            while True:
                print("\nМенеджер задач:")
                print("\tУдаление задач:")
                print("\t\t1. Удалить задачу по ID")
                print("\t\t2. Удалить задач по категории")
                print("\t\t3. Назад")
                choice = input("Выберите опцию: ")
                if choice == '1':
                    """Удаление задачи по ID"""
                    task_id = None
                    try:
                        task_id = int(input("ID задачи для удаления: "))
                    except ValueError:
                        print("Ошибка: Введено некорректное значение. "
                              "Пожалуйста, введите число.")
                        continue

                    manager.delete_task(task_id=task_id)
                elif choice == '2':
                    """Удаление задач по категории"""
                    manager.display_grouped_tasks()
                    tasks_category = input("Категория задач для удаления: ")
                    manager.delete_task(category=tasks_category)
                    pass
                elif choice == '3':
                    """Выход из изменения задачи"""
                    print("\nНазад...")
                    break
                else:
                    print("\nНеверный выбор. Пожалуйста, попробуйте снова.")

        elif choice == '5':
            """Поиск задач по ключевому слову, категории или статусу"""
            keyword = input("Поиск по ключевому слову: ")
            category = input("Поиск по категории: ")
            status = input("Поиск по статусу (Выполнена/Не выполнена): ")
            tasks = manager.search_tasks(None, keyword, category, status)
            manager.display_tasks(tasks)
        elif choice == '6':
            """Выход из программы"""
            print("Выход...")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
