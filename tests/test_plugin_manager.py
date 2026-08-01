from core.plugin_manager import PluginManager


def test_discover_plugins(tmp_path):
    """Тест поиска плагинов в директории."""
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "my_plugin.py").write_text("def run(): pass", encoding="utf-8")
    (plugins_dir / "__init__.py").write_text("", encoding="utf-8")

    pm = PluginManager(str(plugins_dir))
    discovered = pm.discover_plugins()

    assert "my_plugin" in discovered
    assert "__init__" not in discovered


def test_load_sample_plugin():
    """Тест загрузки тестового плагина из папки plugins."""
    pm = PluginManager("plugins")
    module = pm.load_plugin("sample_plugin")

    assert hasattr(module, "initialize")
    assert module.initialize() is True
