# 📝 CLI Notes

[![Build](https://github.com/CoderDeltaLAN/cli-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/CoderDeltaLAN/cli-notes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
![Lint: Ruff](https://img.shields.io/badge/lint-ruff-46a2f1)

Una **aplicación de línea de comandos (CLI)** para gestionar notas simples, construida en **Python** con **Poetry**, **pytest**, **pre-commit** y **CI/CD**.  
Las notas se guardan en `~/.local/share/cli-notes/notes.json`.

---

## 🚀 Requisitos
- Python 3.12
- Poetry

---

## 🔧 Instalación

Clona el repositorio y entra en la carpeta:

```bash
git clone https://github.com/CoderDeltaLAN/cli-notes.git
cd cli-notes
poetry install
```

---

## 📖 Uso rápido 

Añadir una nota:

```bash
poetry run python -m cli_notes add "It works on my machine 🤷"
```

Listar notas:

```bash
poetry run python -m cli_notes list
```

Borrar una nota:

```bash
poetry run python -m cli_notes remove 1
```

---

## 📜 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

## ✨ Frase inspiradora para programadores

> "It works on my machine 🤷"

