from pathlib import Path
from typing import Any

from cli_notes.__main__ import add_note, list_notes, remove_note


def test_remove_borra_por_id(tmp_path: Path, monkeypatch: Any) -> None:
    db = tmp_path / "notes.json"
    monkeypatch.setenv("CLI_NOTES_DB", str(db))

    add_note("A")
    add_note("B")
    add_note("C")

    assert len(list_notes()) == 3

    ok = remove_note(2)
    assert ok is True

    notas = list_notes()
    assert len(notas) == 2
    assert [n.text for n in notas] == ["A", "C"]
    assert [n.id for n in notas] == [1, 2]  # reindex sencillo
