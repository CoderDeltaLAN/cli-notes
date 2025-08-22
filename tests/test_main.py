from typing import Any
from cli_notes.__main__ import main


def test_main(capsys: Any) -> None:
    main()
    captured = capsys.readouterr()
    assert "Hola" in captured.out
