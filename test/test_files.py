import pytest
import json
from unittest.mock import patch, mock_open

from task_manager import TaskManager, Task


@pytest.fixture
def setup_task_manager():
    """Фикстура для создания временного экземпляра TaskManager."""
    manager = TaskManager(filename="test_tasks.json")
    manager.tasks = []  # Изоляция теста (отсутствие задач)
    manager.next_id = 1  # Сброс ID задач
    return manager


@pytest.mark.parametrize("file_data, expected_task_count, expected_return", [
    (json.dumps({
        'tasks': [
            {'id': 1, 'title': 'Задача 1', 'description': 'Описание задачи 1',
             'category': 'Работа', 'due_date': '05.12.2024',
             'priority': 'Средний', 'status': 'Не выполнена'},
            {'id': 2, 'title': 'Задача 2', 'description': 'Описание задачи 2',
             'category': 'Учеба', 'due_date': '06.12.2024',
             'priority': 'Высокий', 'status': 'Не выполнена'}
        ],
        'next_id': 3
    }), 2, True),  # Когда файл с корректными данными
    (None, 0, False),  # Когда файл не найден
    ('{invalid_json', 0, False)  # Когда файл поврежден (невалидный JSON)
])
def test_load_data(setup_task_manager, file_data,
                   expected_task_count, expected_return):
    """Тест для функции load_data с различными данными"""
    if file_data == '{invalid_json':
        with patch("builtins.open", mock_open(read_data=file_data)):
            result = setup_task_manager.load_data()
            assert result == expected_return
            assert len(setup_task_manager.tasks) == expected_task_count
    elif file_data:
        with patch("builtins.open", mock_open(read_data=file_data)):
            result = setup_task_manager.load_data()
            assert result == expected_return
            assert len(setup_task_manager.tasks) == expected_task_count
    else:
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = setup_task_manager.load_data()
            assert result == expected_return
            assert len(setup_task_manager.tasks) == expected_task_count


@pytest.mark.parametrize("tasks_to_save, expected_task_count, expected_return",
                         [
                             # Сохранение одной задачи
                             ([Task(1, "Задача 1", "Описание задачи 1",
                                    "Работа", "05.12.2024", "Средний")],
                              1, True),
                         ])
def test_save_data_success(setup_task_manager, tasks_to_save,
                           expected_task_count, expected_return):
    """Тест для функции save_data с успешной записью данных."""

    mock_data = {
        'tasks': [task.to_dict() for task in tasks_to_save],
        'next_id': len(tasks_to_save) + 1
    }

    with patch("builtins.open", mock_open()) as mock_file:
        setup_task_manager.tasks = tasks_to_save
        setup_task_manager.next_id = len(tasks_to_save) + 1

        result = setup_task_manager.save_data()

        assert result == expected_return

        assert len(setup_task_manager.tasks) == expected_task_count

        if expected_return:
            expected_json = json.dumps(mock_data, ensure_ascii=False, indent=4)

            written_data = "".join(
                [call[0][0] for call in mock_file().write.call_args_list])

            assert written_data.strip() == expected_json.strip()


def test_save_data_error_handling(setup_task_manager):
    """Тест для функции save_data с ошибкой записи в файл."""

    with patch("builtins.open", side_effect=IOError("Ошибка записи в файл")):
        result = setup_task_manager.save_data()
        assert result is False
