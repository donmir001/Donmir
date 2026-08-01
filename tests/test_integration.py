from main import main


def test_full_system_integration(capsys):
    """Сквозной интеграционный тест работы всей платформы."""
    main()
    captured = capsys.readouterr()
    assert "Привет! Я" in captured.out
    assert "Платформа полностью активна!" in captured.out
