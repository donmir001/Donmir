from core.event_bus import EventBus


def test_event_bus_subscribe_and_publish():
    """Тест подписки и публикаций событий."""
    bus = EventBus()
    received_data = []

    def handler(data):
        received_data.append(data)

    bus.subscribe("test_event", handler)
    bus.publish("test_event", "Hello Event")

    assert len(received_data) == 1
    assert received_data[0] == "Hello Event"


def test_event_bus_unsubscribe():
    """Тест отписки от событий."""
    bus = EventBus()
    received_data = []

    def handler(data):
        received_data.append(data)

    bus.subscribe("test_event", handler)
    bus.unsubscribe("test_event", handler)
    bus.publish("test_event", "Hello Again")

    assert len(received_data) == 0
