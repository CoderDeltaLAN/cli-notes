from typing import Any
from paquete_ejemplo.__main__ import main


def test_main(capsys: Any) -> None:
    main()
    captured = capsys.readouterr()
    assert "Hola desde paquete_ejemplo" in captured.out
