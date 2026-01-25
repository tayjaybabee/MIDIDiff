# MIDIDiff - Sourcery AI Instructions

This document provides guidance for Sourcery AI when reviewing and refactoring code in the MIDIDiff project.

## Project Overview

MIDIDiff is a Python CLI tool that compares MIDI files and generates diff files. The project emphasizes:
- **Clean architecture** with strict module separation of concerns
- **Type safety** with comprehensive type hints
- **Immutable data structures** for reliability
- **User-friendly CLI** with helpful error messages

## Critical Design Principles

### 1. Module Separation of Concerns

**MOST IMPORTANT:** Each module must have a single, well-defined responsibility.

#### Current Module Structure:

```
midi_diff/
├── core.py           # Core MIDI diff algorithm
├── midi_utils.py     # MIDI file parsing and NoteEvent data model
└── cli/              # CLI-specific code
    ├── __init__.py   # CLI entry point
    ├── main.py       # Argument parsing and command routing
    ├── version.py    # Version display and update checking
    └── docs.py       # Documentation opening functionality
```

#### Rules for Module Separation:

1. **DO NOT suggest moving functions between modules** unless they clearly belong to a different concern
2. **DO suggest creating new modules** when adding functionality that doesn't fit existing modules
3. **DO NOT suggest consolidating** version.py and docs.py into main.py
4. **DO suggest splitting** a module if it handles multiple unrelated concerns

**Examples:**

✅ **Good:**
- Create `cli/export.py` for export-related commands
- Create `cli/stats.py` for statistics functionality
- Keep version checking in `version.py`
- Keep documentation opening in `docs.py`

❌ **Bad:**
- Move `open_documentation()` from `docs.py` to `main.py`
- Combine `version.py` and `docs.py` into one file
- Add export functions to `core.py`

### 2. Type Hints

**Required:** All public functions must have complete type hints.

```python
# ✅ Good
def process_file(path: Path, mode: str = "read") -> MidiFile:
    ...

# ❌ Bad
def process_file(path, mode="read"):
    ...
```

**Guidelines:**
- Use `typing.Final` for constants
- Use `pathlib.Path` instead of `str` for file paths
- Use `Sequence[str]` for argument lists (more flexible than `list[str]`)
- Prefer concrete types over `Any`

### 3. Immutability

The project uses immutable data structures where possible:

```python
@dataclass(frozen=True, slots=True)
class NoteEvent:
    pitch: int
    start: int
    duration: int
    velocity: int
```

**DO NOT suggest** removing `frozen=True` or making data classes mutable unless there's a compelling reason.

### 4. Error Handling

**User-friendly errors over exceptions:**

```python
# ✅ Good - helpful message, graceful handling
try:
    webbrowser.open(url)
except Exception as e:
    print(f"Warning: Unable to open browser: {e}")
    print(f"Please visit: {url}")

# ❌ Bad - cryptic error, crashes
webbrowser.open(url)  # May fail silently or crash
```

**Guidelines:**
- Print clear, actionable error messages
- Provide alternatives when operations fail (e.g., manual URL)
- Don't use bare `except:` clauses
- Don't hide errors from users

### 5. Pathlib Over os.path

**Always use `pathlib.Path` for file operations:**

```python
# ✅ Good
from pathlib import Path

def read_file(path: Path) -> str:
    return path.read_text()

# ❌ Bad
import os

def read_file(path: str) -> str:
    return open(os.path.join(path, "file.txt")).read()
```

### 6. Constants and Magic Values

**Extract constants to module level:**

```python
# ✅ Good
DOCUMENTATION_URL: Final[str] = "https://mididiff.readthedocs.io/en/latest/"

def open_documentation() -> None:
    webbrowser.open(DOCUMENTATION_URL)

# ❌ Bad
def open_documentation() -> None:
    webbrowser.open("https://mididiff.readthedocs.io/en/latest/")
```

## Code Style Preferences

### Docstrings

Use Google/NumPy style with clear parameter and return documentation:

```python
def extract_notes(mid: MidiFile) -> list[NoteEvent]:
    """
    Extract note events from a MIDI file.
    
    Parameters:
        mid: The MIDI file to extract notes from.
        
    Returns:
        List of NoteEvent objects representing all notes in the file.
    """
    ...
```

### Import Organization

```python
# Standard library
import argparse
import sys
from pathlib import Path
from typing import Final, Sequence

# Third-party
import mido
from rich.console import Console

# Local
from midi_diff.core import main as core_main
from midi_diff.cli.version import print_version_info
from midi_diff.cli.docs import open_documentation
```

### Naming Conventions

- **Constants:** `UPPER_SNAKE_CASE` with `Final` type hint
- **Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Private functions:** `_leading_underscore`
- **Subcommand constants:** `COMMAND_DIFF`, `COMMAND_DOCS`, etc.

## What NOT to Suggest

1. **DO NOT suggest removing type hints** (e.g., "make code more concise")
2. **DO NOT suggest combining modules** (violates separation of concerns)
3. **DO NOT suggest removing error handling** (user experience is critical)
4. **DO NOT suggest using `os.path`** instead of `pathlib.Path`
5. **DO NOT suggest making data classes mutable** without strong justification
6. **DO NOT suggest removing docstrings** (documentation is important)
7. **DO NOT suggest removing the `COMMAND_*` constants** (they're the single source of truth)

## What TO Suggest

1. **DO suggest extracting magic strings to constants**
2. **DO suggest adding type hints where missing**
3. **DO suggest creating new modules for new concerns**
4. **DO suggest improving error messages**
5. **DO suggest simplifying complex logic** (but keep separation of concerns)
6. **DO suggest adding docstrings where missing**
7. **DO suggest using `pathlib.Path` where `str` paths are used**
8. **DO suggest using `Final` for constants**

## Version and Dependencies

- **Python:** 3.11+ (minimum), 3.13+ (recommended)
- **Build system:** Poetry
- **Key dependency:** mido (MIDI library)
- **Optional dependencies:** rich (CLI formatting)

## Testing

- **Current state:** No automated tests
- **Manual testing:** Build with `poetry build`, test CLI commands
- **DO NOT suggest** adding complex test frameworks unless explicitly requested
- **DO suggest** simple validation approaches

## Changelog and Versioning

- **Format:** [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- **User-facing changes MUST update CHANGELOG.md**
- **Version bumps required for user-facing changes**
- **DO suggest** updating CHANGELOG.md if changes affect users

## File Headers

All files should have author headers:

```python
"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/docs.py

Description:
    Documentation-related functionality for the MIDIDiff CLI.
"""
```

**DO NOT suggest removing these headers.**

## Summary: Sourcery's Role

When reviewing MIDIDiff code:

1. **Enforce module separation** - This is the #1 priority
2. **Improve type hints** - Add where missing, improve specificity
3. **Enhance error handling** - Make errors more user-friendly
4. **Suggest better patterns** - pathlib, constants, etc.
5. **Maintain style** - Follow existing conventions
6. **Respect architecture** - Don't suggest breaking established patterns

**Remember:** This is a small, well-architected project. The goal is to **maintain** its clean structure, not to over-engineer it. Suggestions should improve maintainability without adding unnecessary complexity.

---

**Last Updated:** 2026-01-25  
**Sourcery Configuration:** See `.sourcery.yaml` in repository root
