import pytest

from task import Task
from task_manager import TaskManager


@pytest.mark.parametrize("tasks, expected_output, expected_return", [
    # Случай, когда задачи есть
    (
        [
            Task(1, "Задача 1", "Описание 1", "Работа",
                 "05.12.2024", "Средний"),
            Task(2, "Задача 2", "Описание 2", "Личное",
                 "06.12.2024", "Высокий")
        ],
        (
            "ID: 1, Название: Задача 1, Описание: Описание 1, "
            "Категория: Работа, Срок: 05.12.2024, Приоритет: Средний, "
            "Статус: Не выполнена\n"
            "ID: 2, Название: Задача 2, Описание: Описание 2, "
            "Категория: Личное, Срок: 06.12.2024, Приоритет: Высокий, "
            "Статус: Не выполнена\n"
        ),
        True
    ),
    # Случай, когда задач нет
    (
        [],
        "Задачи не найдены.\n",
        False
    ),
])
def test_display_tasks(capfd, tasks, expected_output, expected_return):
    """Тест для метода display_tasks."""
    result = TaskManager.display_tasks(tasks)
    captured = capfd.readouterr()
    assert captured.out == expected_output
    assert result == expected_return
