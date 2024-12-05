from typing import Dict


class Task:
    """Класс для представления задачи. Содержит атрибуты задачи и методы для
    преобразования объекта в словарь и обратно.

    """
    def __init__(self, id: int, title: str, description: str, category: str,
                 due_date: str, priority: str, status: str = 'Не выполнена'):
        """Инициализирует объект задачи с заданными параметрами.
        :param id: Уникальный идентификатор задачи.
        :param title: Название задачи.
        :param description: Описание задачи.
        :param category: Категория задачи.
        :param due_date: Срок выполнения задачи.
        :param priority: Приоритет задачи ('Низкий', 'Средний', 'Высокий').
        :param status: Статус задачи ('Не выполнена' или 'Выполнена').

        """
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> Dict:
        """Преобразует объект задачи в словарь для хранения в JSON.
        :return: Словарь с данными задачи.

        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'due_date': self.due_date,
            'priority': self.priority,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """Создает объект задачи из словаря.
        :param data: Словарь с данными задачи.
        :return: Объект Task.
        
        """
        return Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            due_date=data['due_date'],
            priority=data['priority'],
            status=data['status']
        )
