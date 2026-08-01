"""Пример простого плагина для проверки загрузчика."""


def initialize(event_bus=None):
    """Функция инициализации плагина."""
    if event_bus:
        event_bus.publish("plugin_loaded", {"plugin": "sample_plugin"})
    return True
