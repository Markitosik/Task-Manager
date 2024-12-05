import pytest
import os

from task_manager import TaskManager


@pytest.fixture
def setup_task_manager():
    """Фикстура для создания временного экземпляра TaskManager."""
    filename = "test_tasks.json"

    if os.path.exists(filename):
        os.remove(filename)

    manager = TaskManager(filename=filename)
    manager.tasks = []  # Изоляция теста (отсутствие задач)
    manager.next_id = 1  # Сброс ID задач
    return manager


@pytest.mark.parametrize("task_id, expected_return, expected_task_count", [
    (1, True, 0),  # Удаление задачи по ID
    (999, False, 1),  # Задача с таким ID не существует
])
def test_delete_task_by_id(setup_task_manager, task_id, expected_return,
                           expected_task_count):
    """Тест для удаления задачи по ID."""
    manager = setup_task_manager

    result = manager.add_task(
        title="Задача с приоритетом",
        description="Описание задачи",
        category="Работа",
        due_date="05.12.2024",
        priority="Средний"
    )

    result = manager.delete_task(task_id=task_id)

    assert result is expected_return
    assert len(manager.tasks) == expected_task_count

    assert len(manager.tasks) == expected_task_count


@pytest.mark.parametrize("category, expected_return, expected_task_count", [
    ("Работа", True, 1),  # Удаление задач в категории
    ("Учеба", False, 2),  # Задачи в категории не найдены
])
def test_delete_task_by_category(setup_task_manager, category, expected_return,
                                 expected_task_count):
    """Тест для удаления задач по категории."""
    manager = setup_task_manager

    result = manager.add_task(
        title="Задача 1",
        description="Описание задачи",
        category="Работа",
        due_date="05.12.2024",
        priority="Средний"
    )
    result = manager.add_task(
        title="Задача 2",
        description="Описание задачи",
        category="Личное",
        due_date="06.12.2024",
        priority="Высокий"
    )

    result = manager.delete_task(category=category)

    assert result is expected_return
    assert len(manager.tasks) == expected_task_count

    assert len(manager.tasks) == expected_task_count


def test_delete_task_no_params(setup_task_manager):
    """Тест для случая, когда не указаны параметры для удаления задачи."""
    manager = setup_task_manager

    result = manager.delete_task()

    assert result is False
