import pytest

from task_manager import TaskManager


@pytest.fixture
def setup_task_manager():
    """Фикстура для создания временного экземпляра TaskManager."""
    manager = TaskManager(filename="test_tasks.json")
    manager.tasks = []  # Изоляция теста (отсутствие задач)
    manager.next_id = 1  # Сброс ID задач
    return manager


@pytest.mark.parametrize("title, expected_return", [
    ("Корректная задача", True),  # Валидное название
    ("", False),  # Невалидное название
])
def test_add_task_title_validation(setup_task_manager, title, expected_return):
    """Тест для валидации поля title (проверка различных типов данных)."""
    manager = setup_task_manager
    result = manager.add_task(
        title=title,
        description="Описание задачи",
        category="Работа",
        due_date="05.12.2024",
        priority="Средний"
    )

    if expected_return:
        assert result is True
        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.title == title
    else:
        assert result is False
        assert len(manager.tasks) == 0


@pytest.mark.parametrize("description, expected_return", [
    ("Описание задачи", True),  # Валидное описание
    ("", False),  # Невалидное описание
])
def test_add_task_description_validation(setup_task_manager, description,
                                         expected_return):
    """Тест для валидации поля description
    (проверка различных типов данных)."""
    manager = setup_task_manager
    result = manager.add_task(
        title="Задача с описанием",
        description=description,
        category="Работа",
        due_date="05.12.2024",
        priority="Средний"
    )

    if expected_return:
        assert result is True
        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.description == description
    else:
        assert result is False
        assert len(manager.tasks) == 0


@pytest.mark.parametrize("category, expected_return", [
    ("Работа", True),  # Валидная категория
    ("", False),  # Невалидная категория

])
def test_add_task_category_validation(setup_task_manager, category,
                                      expected_return):
    """Тест для валидации поля category (проверка различных типов данных)."""
    manager = setup_task_manager
    result = manager.add_task(
        title="Задача с категорией",
        description="Описание задачи",
        category=category,
        due_date="05.12.2024",
        priority="Средний"
    )

    if expected_return:
        assert result is True
        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.category == category
    else:
        assert result is False
        assert len(manager.tasks) == 0


@pytest.mark.parametrize("due_date, expected_return", [
    ("05.12.2024", True),  # Валидная дата
    ("12-05-2024", False),  # Невалидный формат даты
])
def test_add_task_due_date_validation(setup_task_manager, due_date,
                                      expected_return):
    """Тест для валидации поля due_date (проверка даты)."""
    manager = setup_task_manager
    result = manager.add_task(
        title="Задача с датой",
        description="Описание задачи",
        category="Работа",
        due_date=due_date,
        priority="Средний"
    )

    if expected_return:
        assert result is True
        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.due_date == due_date
    else:
        assert result is False
        assert len(manager.tasks) == 0


@pytest.mark.parametrize("priority, expected_return", [
    ("Средний", True),  # Валидный приоритет
    ("Очень высокий", False),  # Невалидный приоритет
])
def test_add_task_priority_validation(setup_task_manager, priority,
                                      expected_return):
    """Тест для валидации поля priority (проверка приоритета)."""
    manager = setup_task_manager
    result = manager.add_task(
        title="Задача с приоритетом",
        description="Описание задачи",
        category="Работа",
        due_date="05.12.2024",
        priority=priority,
    )

    if expected_return:
        assert result is True
        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.priority == priority
    else:
        assert result is False
        assert len(manager.tasks) == 0
