import pytest
import os

from task import Task
from task_manager import TaskManager


@pytest.fixture
def setup_task_manager():
    """Фикстура для создания временного экземпляра TaskManager с
    реальным файлом.

    """
    filename = "test_tasks.json"

    if os.path.exists(filename):
        os.remove(filename)

    manager = TaskManager(filename=filename)
    manager.tasks = []  # Сброс задач перед тестом
    manager.next_id = 1  # Сброс ID задач
    return manager


@pytest.fixture
def add_sample_tasks(setup_task_manager):
    """Фикстура для добавления задач в TaskManager, сохранения их
    в файл и возвращения.

    """
    manager = setup_task_manager
    tasks = [
        Task(1, "Задача с приоритетом", "Описание задачи", "Работа",
             "05.12.2024", "Средний"),
        Task(2, "Задача с высоким приоритетом", "Описание задачи", "Учеба",
             "06.12.2024", "Высокий"),
        Task(3, "Задача с низким приоритетом", "Описание задачи", "Личное",
             "07.12.2024", "Низкий")
    ]

    manager.tasks.extend(tasks)
    manager.save_data()

    return manager, tasks


@pytest.mark.parametrize("search_params, expected_task_count, expected_titles",
                         [
                             # Поиск по ID
                             ({"task_id": 1}, 1, ["Задача с приоритетом"]),
                             # Поиск по ключевому слову
                             ({"keyword": "приоритет"}, 3,
                              ["Задача с приоритетом",
                               "Задача с высоким приоритетом",
                               "Задача с низким приоритетом"]),
                             # Поиск по категории
                             ({"category": "Работа"}, 1,
                              ["Задача с приоритетом"]),
                             # Поиск по статусу
                             ({"status": "Не выполнена"}, 3,
                              ["Задача с приоритетом",
                               "Задача с высоким приоритетом",
                               "Задача с низким приоритетом"]),
                             # Задача с таким ID не найдена
                             ({"task_id": 999}, 0, []),
                             # Ключевое слово не найдено
                             ({"keyword": "не существует"}, 0, []),
                             # Категория не найдена
                             ({"category": "Не существует"}, 0, []),
                             # Статус не найден
                             ({"status": "Не существует"}, 0, []),
                         ])
def test_search_tasks(setup_task_manager, add_sample_tasks, search_params,
                      expected_task_count, expected_titles):
    """Тест для поиска задач по различным параметрам."""
    manager, tasks = add_sample_tasks

    result = manager.search_tasks(**search_params)

    assert len(result) == expected_task_count

    result_titles = [task.title for task in result]
    assert result_titles == expected_titles
