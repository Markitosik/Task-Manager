import pytest

from task import Task
from task_manager import TaskManager


@pytest.mark.parametrize("tasks, expected_return, expected_category_counts", [
    # Нет задач
    ([], False, {}),

    # Одна задача
    ([Task(1, "Задача с приоритетом", "Описание задачи", "Работа",
           "05.12.2024", "Средний", "Не выполнена")],
     True, {"Работа": 1}),

    # Несколько задач, каждая в своей категории
    ([Task(1, "Задача с приоритетом", "Описание задачи", "Работа",
           "05.12.2024", "Средний", "Не выполнена"),
      Task(2, "Личная задача", "Описание задачи", "Личное",
           "06.12.2024", "Низкий", "Выполнена")],
     True, {"Работа": 1, "Личное": 1}),

    # Несколько задач в одной категории и других категориях
    ([Task(1, "Задача с приоритетом", "Описание задачи", "Работа",
           "05.12.2024", "Средний", "Не выполнена"),
      Task(2, "Задача 2", "Описание задачи", "Работа",
           "06.12.2024", "Высокий", "Не выполнена"),
      Task(3, "Задача 3", "Описание задачи", "Личное",
           "07.12.2024", "Низкий", "Выполнена"),
      Task(4, "Задача 4", "Описание задачи", "Здоровье",
           "08.12.2024", "Средний", "Не выполнена"),
      Task(5, "Задача 5", "Описание задачи", "Работа",
           "09.12.2024", "Низкий", "Выполнена"),
      Task(6, "Задача 6", "Описание задачи", "Личное",
           "10.12.2024", "Средний", "Не выполнена")],
     True, {"Работа": 3, "Личное": 2, "Здоровье": 1}),
])
def test_display_grouped_tasks(tasks, expected_return,
                               expected_category_counts):
    """Тестируем функцию display_grouped_tasks на возвращаемое значение
    True/False и на количество задач в каждой категории.

    """
    task_manager = TaskManager()
    task_manager.tasks = tasks

    result = task_manager.display_grouped_tasks()

    assert result == expected_return

    grouped_tasks = task_manager.group_tasks_by_category()
    for category, count in expected_category_counts.items():
        assert len(grouped_tasks.get(category, [])) == count
