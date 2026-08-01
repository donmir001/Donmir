import pytest
from core.event_bus import EventBus
from executor.task_runner import TaskRunner


def test_task_runner_success():
    """Тест успешного выполнения задачи."""
    bus = EventBus()
    runner = TaskRunner(bus)

    events = []
    bus.subscribe("task_started", lambda d: events.append(d["task_name"]))
    bus.subscribe("task_completed", lambda d: events.append(d["result"]))

    runner.register_task("add", lambda a, b: a + b)
    result = runner.run_task("add", 2, 3)

    assert result == 5
    assert events == ["add", 5]


def test_task_runner_not_found():
    """Тест запуска несуществующей задачи."""
    runner = TaskRunner()
    with pytest.raises(KeyError):
        runner.run_task("non_existent")
