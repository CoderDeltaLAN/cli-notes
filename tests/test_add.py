from pathlib import Path
from typing import Any

from cli_notes.__main__ import add_note, load_notes


def test_add_crea_archivo_y_guarda(tmp_path: Path, monkeypatch: Any) -> None:
    # Redirigimos la DB a una ruta temporal para no tocar el HOME real
    db = tmp_path / "notes.json"
    monkeypatch.setenv("CLI_NOTES_DB", str(db))

    note = add_note("Hola mundo")
    assert db.exists(), "Se debe crear el archivo de base de datos"
    notas = load_notes()
    assert len(notas) == 1
    assert notas[0].text == "Hola mundo"
    assert note.id == 1
