import pytest

from task import Task
from task_manager import TaskManager


@pytest.fixture
def setup_task_manager():
    """Фикстура для создания временного экземпляра TaskManager."""
    manager = TaskManager(filename="test_tasks.json")
    manager.tasks = []  # Изоляция теста (отсутствие задач)
    manager.next_id = 1  # Сброс ID задач
    return manager


@pytest.fixture
def add_sample_task(setup_task_manager):
    """Фикстура для добавления задачи в TaskManager."""
    manager = setup_task_manager
    task = Task(1, "Задача с приоритетом", "Описание задачи", "Работа",
                "05.12.2024", "Средний")
    manager.tasks.append(task)
    return manager, task


@pytest.mark.parametrize("update_data, expected_title, expected_return", [
    # Обновление названия
    ({"title": "Обновленное название"}, "Обновленное название", True),
    # Обновление описания
    ({"description": "Обновленное описание"}, "Описание задачи", True),
    ({"category": "Личное"}, "Работа", True),  # Обновление категории
    ({"due_date": "06.12.2024"}, "05.12.2024", True),  # Обновление даты
    ({"priority": "Высокий"}, "Средний", True),  # Обновление приоритета
    ({"status": "Выполнена"}, "Не выполнена", True),  # Обновление статуса
])
def test_update_task_valid_data(add_sample_task, update_data, expected_title,
                                expected_return):
    """Тестируем обновление задачи с валидными данными."""

    manager, task = add_sample_task

    result = manager.update_task(task.id, **update_data)

    assert result is expected_return

    if update_data.get("title"):
        assert task.title == expected_title
    elif update_data.get("description"):
        assert task.description == update_data["description"]
    elif update_data.get("category"):
        assert task.category == update_data["category"]
    elif update_data.get("due_date"):
        assert task.due_date == update_data["due_date"]
    elif update_data.get("priority"):
        assert task.priority == update_data["priority"]
    elif update_data.get("status"):
        assert task.status == update_data["status"]


def test_update_non_existent_task(setup_task_manager):
    """Тестируем обновление задачи, которая не существует."""

    manager = setup_task_manager

    result = manager.update_task(999, title="Новая задача",
                                 description="Описание", category="Личное")

    assert result is False


@pytest.mark.parametrize("field, invalid_value, expected_return", [
    ("title", 11, False),  # Невалидное название
    ("description", 11, False),  # Невалидное описание
    ("category", 11, False),  # Невалидная категория
    ("due_date", "2024/12/05", False),  # Невалидный формат даты
    ("priority", "Очень высокий", False),  # Невалидный приоритет
    ("status", "Не известно", False),  # Невалидный статус
])
def test_update_task_invalid_data(add_sample_task, field, invalid_value,
                                  expected_return):
    """Тестируем обновление задачи с невалидными данными."""

    manager, task = add_sample_task

    update_data = {field: invalid_value}
    result = manager.update_task(task.id, **update_data)

    assert result is expected_return

    if field == "title":
        assert task.title == "Задача с приоритетом"
    elif field == "description":
        assert task.description == "Описание задачи"
    elif field == "category":
        assert task.category == "Работа"
    elif field == "due_date":
        assert task.due_date == "05.12.2024"
    elif field == "priority":
        assert task.priority == "Средний"
    elif field == "status":
        assert task.status == "Не выполнена"
