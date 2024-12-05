import pytest

from task_manager import TaskManager


@pytest.mark.parametrize("category, is_valid", [
    ("Работа", True),  # Валидная категория
    ("", False),  # Пустая категория
    (None, False),  # None вместо строки
    (123, False),  # Число вместо строки
    (["Работа"], False),  # Список вместо строки
    ({"category": "Работа"}, False),  # Словарь вместо строки
])
def test_validate_string(category, is_valid):
    """Тест для функции validate_string."""
    result = TaskManager.validate_string(category, "Категория")
    assert result == is_valid


@pytest.mark.parametrize("date, is_valid", [
    ("05.12.2024", True),  # Валидная дата
    ("2024.12.05", False),  # Неверный формат
    ("12-05-2024", False),  # Неверный формат
    ("", False),  # Пустая строка
    (None, False),  # None вместо строки
    (123, False),  # Число вместо строки
    (["05.12.2024"], False),  # Список вместо строки
    ({"05.12.2024": "05.12.2024"}, False),  # Словарь вместо строки
])
def test_is_valid_date(date, is_valid):
    """Тест для функции is_valid_date."""
    result = TaskManager.is_valid_date(date)
    assert result == is_valid


@pytest.mark.parametrize("priority, is_valid", [
    ("Низкий", True),  # Валидный приоритет
    ("Средний", True),  # Валидный приоритет
    ("Высокий", True),  # Валидный приоритет
    ("Высокий+", False),  # Неверный приоритет
    ("", False),  # Пустая строка
    (None, False),  # None вместо строки
    (123, False),  # Число вместо строки
    (["Низкий"], False),  # Список вместо строки
    ({"Низкий": "Низкий"}, False),  # Словарь вместо строки
])
def test_is_valid_priority(priority, is_valid):
    """Тест для функции is_valid_priority."""
    result = TaskManager.is_valid_priority(priority)
    assert result == is_valid


@pytest.mark.parametrize("status, is_valid", [
    ("Выполнена", True),  # Валидный статус
    ("Не выполнена", True),  # Валидный статус
    ("Завершена", False),  # Некорректный статус
    ("", False),  # Пустая строка
    (None, False),  # None вместо строки
    (123, False),  # Число вместо строки
    (["Выполнена"], False),  # Список вместо строки
    ({"Выполнена": "Выполнена"}, False),  # Словарь вместо строки
])
def test_is_valid_status(status, is_valid):
    """Тест для функции is_valid_status."""
    result = TaskManager.is_valid_status(status)
    assert result == is_valid
