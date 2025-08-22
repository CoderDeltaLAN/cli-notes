from pathlib import Path
from typing import Any

from cli_notes.__main__ import add_note, list_notes


def test_list_devuelve_notas(tmp_path: Path, monkeypatch: Any) -> None:
    db = tmp_path / "notes.json"
    monkeypatch.setenv("CLI_NOTES_DB", str(db))

    add_note("Primera")
    add_note("Segunda")

    notas = list_notes()
    assert len(notas) == 2
    assert notas[0].text == "Primera"
    assert notas[1].text == "Segunda"
