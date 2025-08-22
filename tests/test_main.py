from pathlib import Path
from typing import Any
import sys

from cli_notes.__main__ import main


def test_main_add(tmp_path: Path, monkeypatch: Any, capsys: Any) -> None:
    # Redirigimos la DB a un archivo temporal
    db = tmp_path / "notes.json"
    monkeypatch.setenv("CLI_NOTES_DB", str(db))

    # Simulamos: cli-notes add "Hola"
    monkeypatch.setattr(sys, "argv", ["cli-notes", "add", "Hola"])

    main()

    out = capsys.readouterr().out
    assert "Nota #1 creada" in out
    assert db.exists()
