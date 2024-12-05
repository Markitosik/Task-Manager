import json
import re
from task import Task
from typing import List


class TaskManager:
    """Класс для управления списком задач. Поддерживает создание, обновление,
    удаление, сохранение, поиск и вывод задач.

    """
    def __init__(self, filename: str = 'tasks.json'):
        """Инициализация менеджера задач. Загружает задачи из файла или создает
        пустой список, если файл отсутствует.

        """
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_data()

    def load_data(self) -> bool:
        """Загружает данные из JSON-файла. Если файл отсутствует или поврежден,
        создает пустой список задач.
        :return: True, если данные успешно загружены, иначе False.

        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task)
                              for task in data.get('tasks', [])]
                self.next_id = data.get('next_id', 1)
            print("Данные успешно загружены.")
            return True
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не найден. "
                  f"Будет создан новый файл.")
            self.tasks = []
            self.next_id = 1
            return False
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле '{self.filename}'. "
                  f"Файл может быть поврежден.")
            self.tasks = []
            self.next_id = 1
            return False

    def save_data(self):
        """Сохраняет данные о задачах в JSON-файл.
        :return: True, если данные успешно сохранены, иначе False.

        """
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Обновленный список задач успешно сохранен в файл "
                  f"'{self.filename}'.")
            return True
        except (IOError, OSError):
            print(f"Не удалось сохранить обновленный список задач в файл "
                  f"'{self.filename}'.")
            return False

    @staticmethod
    def validate_string(value: str, field_name: str) -> bool:
        """Проверяет, что строка не пустая.
        :param value: Проверяемая строка.
        :param field_name: Название поля для отображения в случае ошибки.
        :return: True, если строка валидна, иначе False.

        """
        if not value or not isinstance(value, str):
            print(f"Ошибка: Графа '{field_name}' не может быть пустой и "
                  f"должна быть строкой.")
            return False
        return True

    @staticmethod
    def is_valid_date(date: str) -> bool:
        """Проверяет, что дата соответствует формату dd.mm.yyyy.
        :param date: Строка даты для проверки.
        :return: True, если дата валидна, иначе False.

        """
        # Проверяем, что дата - это строка
        if not isinstance(date, str):
            print("Ошибка: Дата должна быть строкой.")
            return False

        # Проверка на соответствие формату dd.mm.yyyy
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
            print("Ошибка: Неверный формат даты. Ожидается dd.mm.yyyy.")
            return False

        print("Дата валидная.")
        return True

    @staticmethod
    def is_valid_priority(priority: str) -> bool:
        """Проверяет, что приоритет находится в допустимых значениях.
        :param priority: Приоритет задачи ('Низкий', 'Средний', 'Высокий').
        :return: True, если приоритет валиден, иначе False.

        """
        if priority not in ['Низкий', 'Средний', 'Высокий']:
            print("Ошибка: Приоритет должен быть 'Низкий', 'Средний' или "
                  "'Высокий'.")
            return False
        print("Приоритет валидный.")
        return True

    @staticmethod
    def is_valid_status(status: str) -> bool:
        """Проверяет, что статус находится в допустимых значениях.
        :param status: Статус задачи ('Выполнена', 'Не выполнена').
        :return: True, если статус валиден, иначе False.

        """
        if status not in ['Выполнена', 'Не выполнена']:
            print("Ошибка: Статус должен быть 'Выполнена' или 'Не выполнена'.")
            return False
        print("Статус валидный.")
        return True

    def add_task(self, title: str, description: str, category: str,
                 due_date: str, priority: str) -> bool:
        """Добавляет новую задачу.
        :param title: Название задачи.
        :param description: Описание задачи.
        :param category: Категория задачи.
        :param due_date: Срок выполнения задачи.
        :param priority: Приоритет задачи.
        :return: True, если задача успешно добавлена, иначе False.

        """
        print("Создаем задачу...")

        if not self.validate_string(title, "Название"):
            return False
        if not self.validate_string(description, "Описание"):
            return False
        if not self.validate_string(category, "Категория"):
            return False
        if not self.is_valid_date(due_date):
            return False
        if not self.is_valid_priority(priority):
            return False

        new_task = Task(self.next_id, title, description, category, due_date,
                        priority)
        self.tasks.append(new_task)
        print("Задача успешно создана.")
        self.next_id += 1

        return self.save_data()

    def update_task(self, task_id: int, title: str = None,
                    description: str = None, category: str = None,
                    due_date: str = None, priority: str = None,
                    status: str = None):
        """Обновляет данные существующей задачи.
        :param task_id: ID задачи для обновления.
        :param title: Новое название задачи.
        :param description: Новое описание задачи.
        :param category: Новая категория задачи.
        :param due_date: Новый срок выполнения задачи.
        :param priority: Новый приоритет задачи.
        :param status: Новый статус задачи.
        :return: True, если задача успешно обновлена, иначе False.

        """
        print("Обновляем задачу...")
        tasks = self.search_tasks(task_id)
        if not tasks:
            return False
        task = tasks[0]

        if title and not self.validate_string(title, "Название"):
            return False
        if description and not self.validate_string(description, "Описание"):
            return False
        if category and not self.validate_string(category, "Категория"):
            return False
        if due_date and not self.is_valid_date(due_date):
            return False
        if priority and not self.is_valid_priority(priority):
            return False
        if status and not self.is_valid_status(status):
            return False

        if title:
            task.title = title
        if description:
            task.description = description
        if category:
            task.category = category
        if due_date:
            task.due_date = due_date
        if priority:
            task.priority = priority
        if status:
            task.status = status
        print("Задача успешно обновлена.")

        return self.save_data()

    def delete_task(self, task_id: int = None, category: str = None):
        """Удаляет задачу по ID или по категории.
        :param task_id: ID задачи для удаления.
        :param category: Категория для удаления всех задач.
        :return: True, если задача(и) успешно удалены, иначе False.

        """
        print("Удаляем задачу...")

        if task_id:
            tasks = self.search_tasks(task_id=task_id)
            if not tasks:
                print(f"Задача с ID {task_id} не найдена.")
                return False

            self.tasks = [task for task in self.tasks if task.id != task_id]
            print(f"Задача с ID {task_id} удалена.")

        elif category:
            tasks_in_category = [task for task in self.tasks
                                 if task.category.lower() == category.lower()]
            if not tasks_in_category:
                print(f"Задачи в категории '{category}' не найдены.")
                return False

            self.tasks = [task for task in self.tasks
                          if task.category.lower() != category.lower()]
            print(f"Все задачи в категории '{category}' удалены.")

        else:
            print("Не указана ни задача для удаления, "
                  "ни категория для удаления.")
            return False

        return self.save_data()

    def group_tasks_by_category(self):
        """Группирует задачи по категориям.
        :return: Словарь, где ключ — категория, значение — список задач.

        """
        grouped_tasks = {}
        for task in self.tasks:
            if task.category not in grouped_tasks:
                grouped_tasks[task.category] = []
            grouped_tasks[task.category].append(task)
        return grouped_tasks

    def display_grouped_tasks(self):
        """Выводит задачи, сгруппированные по категориям, в консоль.
        :return: True, если задачи были выведены, иначе False.

        """
        grouped_tasks = self.group_tasks_by_category()
        if not grouped_tasks:
            print("Нет задач для отображения.")
            return False
        for category, tasks in grouped_tasks.items():
            print(f"\nКатегория: '{category}'")
            self.display_tasks(tasks)
        return True

    def search_tasks(self, task_id: int = None, keyword: str = None,
                     category: str = None, status: str = None):
        """Выполняет поиск задач по различным параметрам.
        :param task_id: ID задачи для поиска.
        :param keyword: Ключевое слово для поиска в названии и описании.
        :param category: Категория задач для поиска.
        :param status: Статус задач для поиска.
        :return: Список найденных задач.

        """
        results = self.tasks
        if task_id:
            results = [task for task in results if task_id == task.id]
            if not results:
                print(f"Предупреждение: Задача с ID {task_id} не найдена.")
                return results
        if keyword:
            results = [task for task in results
                       if keyword.lower() in task.title.lower() or
                       keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results
                       if category.lower() in task.category.lower()]
        if status:
            results = [task for task in results
                       if status.lower() == task.status.lower()]
        return results

    @staticmethod
    def display_tasks(tasks: List[Task]):
        """Выводит список задач в консоль.
        :param tasks: Список задач для отображения.
        :return: True, если задачи найдены, иначе False.

        """
        if not tasks:
            print("Задачи не найдены.")
            return False
        for task in tasks:
            print(f"ID: {task.id}, Название: {task.title}, "
                  f"Описание: {task.description}, Категория: {task.category}, "
                  f"Срок: {task.due_date}, Приоритет: {task.priority}, "
                  f"Статус: {task.status}")
        return True
