from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List


# Ruta de la base de datos: por defecto en ~/.local/share/cli-notes/notes.json
# En tests se puede sobreescribir con la variable de entorno CLI_NOTES_DB
def db_path() -> Path:
    env = os.getenv("CLI_NOTES_DB")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".local" / "share" / "cli-notes" / "notes.json"


@dataclass
class Note:
    id: int
    text: str
    created_at: str  # ISO 8601


def load_notes() -> List[Note]:
    path = db_path()
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Note(**n) for n in data]


def save_notes(notes: List[Note]) -> None:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [asdict(n) for n in notes]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_note(text: str) -> Note:
    notes = load_notes()
    next_id = (notes[-1].id + 1) if notes else 1
    note = Note(
        id=next_id, text=text, created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z"
    )
    notes.append(note)
    save_notes(notes)
    return note


# ---- CLI ----
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cli-notes", description="CLI de notas sencilla")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Añadir una nueva nota")
    p_add.add_argument("text", help="Contenido de la nota")
    p_add.set_defaults(func=lambda args: print(f"✅ Nota #{add_note(args.text).id} creada"))

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    # Cada subcomando define func
    args.func(args)


if __name__ == "__main__":
    main()
