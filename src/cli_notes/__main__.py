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
    # Nota: utcnow() deprecated; para simplicidad en plantilla seguimos así.
    note = Note(
        id=next_id,
        text=text,
        created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
    )
    notes.append(note)
    save_notes(notes)
    return note


def remove_note(note_id: int) -> bool:
    """Elimina la nota por id. Devuelve True si borró, False si no existía."""
    notes = load_notes()
    new = [n for n in notes if n.id != note_id]
    if len(new) == len(notes):
        return False
    # Reasignamos IDs para mantener consecutivo (opcional; simple para plantilla)
    for idx, n in enumerate(new, start=1):
        n.id = idx
    save_notes(new)
    return True


def list_notes() -> List[Note]:
    """Devuelve la lista de notas (orden natural por id)."""
    return load_notes()


# ---- CLI ----
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cli-notes", description="CLI de notas sencilla")
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Añadir una nueva nota")
    p_add.add_argument("text", help="Contenido de la nota")
    p_add.set_defaults(func=lambda args: print(f"✅ Nota #{add_note(args.text).id} creada"))

    # list
    p_list = sub.add_parser("list", help="Listar notas guardadas")
    p_list.set_defaults(func=_cmd_list)

    # remove
    p_rm = sub.add_parser("remove", help="Borrar una nota por id")
    p_rm.add_argument("id", type=int, help="ID de la nota")
    p_rm.set_defaults(func=_cmd_remove)

    return parser


def _cmd_list(_: argparse.Namespace) -> None:
    notes = list_notes()
    if not notes:
        print("No hay notas todavía.")
        return

    # calcular anchos
    id_w = max(len("ID"), max(len(str(n.id)) for n in notes))
    date_w = max(len("FECHA"), max(len(n.created_at) for n in notes))
    # el texto lo dejamos flexible

    # encabezado
    header = f"{'ID'.ljust(id_w)}  {'FECHA'.ljust(date_w)}  TEXTO"
    sep = f"{'-'*id_w}  {'-'*date_w}  {'-'*5}"
    print(header)
    print(sep)

    # filas
    for n in notes:
        print(f"{str(n.id).ljust(id_w)}  {n.created_at.ljust(date_w)}  {n.text}")


def _cmd_remove(args: argparse.Namespace) -> None:
    ok = remove_note(args.id)
    if ok:
        print(f"🗑️ Nota #{args.id} borrada")
    else:
        print(f"⚠️ Nota #{args.id} no existe")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
