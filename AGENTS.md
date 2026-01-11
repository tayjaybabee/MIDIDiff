# MIDIDiff - Agent Instructions

## Repository Overview

MIDIDiff is a Python command-line tool that compares two MIDI files and generates a "diff" MIDI file containing only the notes that differ between them. The tool extracts note events from both input files, computes the set difference, and outputs the unique notes as a new MIDI file.

**Project Type:** Python CLI application / Python package  
**Size:** Small (~400 lines of Python code across 4 files)  
**Language:** Python (requires Python 3.13+)  
**Build System:** Poetry (using poetry-core as build backend)  
**Key Dependency:** mido (>=1.3.3,<2.0.0) - MIDI file parsing library

## Critical Build Requirements

### Python Version Requirement
- **REQUIRED:** Python 3.13 or higher (specified in `pyproject.toml` as `requires-python = ">=3.13,<4.0"`)
- **CRITICAL:** Poetry will fail to install if Python 3.13+ is not available
- If you encounter "not supported by the project" errors, verify Python version with `python3 --version`

### Build Tools
- **Poetry:** Required for dependency management and building
- Install if missing: `pip install poetry`
- Current tested version: Poetry 2.2.1

## Build and Validation Process

### Bootstrap & Install (ALWAYS run in this order)

1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```
   - Creates a virtual environment automatically
   - Installs `mido` and `packaging` dependencies
   - Installs the package in development mode
   - **Expected time:** 10-30 seconds on first run
   - **Generates:** `poetry.lock` file (DO NOT commit if it doesn't already exist)

### Build Process

```bash
poetry build
```
- Builds both wheel (`.whl`) and source distribution (`.tar.gz`)
- Output location: `dist/` directory
- Build artifacts: `midi_diff-1.0.0.dev2-py3-none-any.whl` and `midi_diff-1.0.0.dev2.tar.gz`
- **Expected time:** 5-10 seconds
- **IMPORTANT:** The `dist/` directory is in `.gitignore` and should NOT be committed

### Testing the CLI

The package provides a `midi-diff` command-line tool:

```bash
# Using poetry run:
poetry run midi-diff fileA.mid fileB.mid output.mid

# After installing the wheel:
pip install dist/*.whl
midi-diff fileA.mid fileB.mid output.mid
```

**Usage:** Requires exactly 3 arguments: two input MIDI files and one output path  
**Expected output:** Prints note counts and saves diff MIDI file

### Manual Testing
- The CLI does not have `--help` or `--version` flags
- Running without arguments shows usage message: "Usage: python -m midi_diff.cli fileA.mid fileB.mid diff.mid"
- To test functionality, you need actual MIDI files

## Project Structure

```
MIDIDiff/
├── .github/           # GitHub configuration (you are here)
├── .gitignore         # Extensive Python/IDE ignore patterns
├── LICENSE.md         # MIT License (Inspyre Softworks)
├── README.md          # Minimal readme with build instructions
├── pyproject.toml     # Project configuration (PEP 621 format)
├── dist/              # Build artifacts (gitignored)
└── midi_diff/         # Main package directory
    ├── __init__.py    # Package init with legacy main entry point
    ├── cli.py         # Command-line interface (entry point: midi_diff.cli:cli)
    ├── core.py        # Core diff logic and main() function
    └── midi_utils.py  # MIDI parsing utilities and NoteEvent class
```

### Key Files

- **`pyproject.toml`**: Single source of truth for project metadata, dependencies, and build configuration
  - Uses PEP 621 format (modern Python packaging)
  - Entry point: `midi-diff = "midi_diff.cli:cli"`
  - Build backend: `poetry.core.masonry.api`

- **`midi_diff/cli.py`**: CLI entry point
  - Exports `cli()` function called by the `midi-diff` command
  - Validates argument count and calls `core.main()`

- **`midi_diff/core.py`**: Main application logic
  - `main(file_a, file_b, out_file)`: Core diff function
  - `_determine_out_path()`: Prevents overwriting files by auto-incrementing filenames
  - Uses `pathlib.Path` for all file operations

- **`midi_diff/midi_utils.py`**: MIDI processing utilities (229 lines)
  - `NoteEvent`: Immutable dataclass for note representation (pitch, start, duration, velocity)
  - `extract_notes(mid)`: Parses MidiFile into list of NoteEvent objects
  - `notes_to_midi(notes)`: Constructs MidiFile from NoteEvent list
  - **IMPORTANT:** NoteEvent validation enforces MIDI bounds (pitch/velocity: 0-127, duration >= 1)

### Configuration Files

- **`.gitignore`**: Comprehensive (110 lines)
  - Ignores: `__pycache__/`, `*.pyc`, `dist/`, `build/`, `.venv/`, `*.lock`, `.idea/`
  - **NOTE:** `*.lock` is ignored, so `poetry.lock` will not be tracked

## Architecture & Code Organization

### Design Patterns
- **Immutable data model:** `NoteEvent` uses `@dataclass(frozen=True, slots=True)`
- **Set-based diffing:** Uses Python sets for efficient note comparison
- **Path safety:** Auto-increments output filenames to prevent overwrites
- **Error handling:** Graceful error messages, no exceptions raised to caller

### Note Comparison Logic
- Notes are compared by `(pitch, start, duration)` - **velocity is excluded**
- This means notes differing only in velocity are treated as identical
- `extract_notes()` handles overlapping notes via a stack-based approach

### Code Style
- Type hints throughout (uses `typing.Union`, `pathlib.Path`)
- Docstrings in Google/NumPy style with Parameters/Returns sections
- Private functions prefixed with `_` (e.g., `_determine_out_path`, `_validate_int`)
- Author headers in all files crediting "Inspyre Softworks"

## Validation & CI

**IMPORTANT:** This repository currently has NO automated testing or CI/CD pipelines:
- No test files (no `test_*.py` or `*_test.py`)
- No `.github/workflows/` directory
- No linting tools configured (no ruff, black, mypy, flake8)
- No pytest or other test frameworks in dependencies

### Manual Validation Steps
1. Run `poetry install` successfully
2. Run `poetry build` and verify artifacts in `dist/`
3. Test CLI with sample MIDI files if available
4. Verify no unintended changes to `pyproject.toml` version constraints

## Common Issues & Workarounds

### Python Version Mismatch
**Error:** "The currently activated Python version X.X.X is not supported by the project (>=3.13,<4.0)"  
**Solution:** 
- Verify system has Python 3.13+: `python3.13 --version`
- Use `poetry env use python3.13` to set the correct version
- If Python 3.13 is unavailable, this is a blocking issue for installation

### Missing Poetry
**Error:** `poetry: command not found`  
**Solution:** `pip install poetry` or `pip3 install poetry`

### Build Artifacts in Repo
**Issue:** `dist/` directory showing in git status  
**Solution:** It's already in `.gitignore`, run `git status` to confirm it's ignored

## Version Management

**Current version:** `1.0.0-dev.2` (defined in `pyproject.toml`)

### When to Bump Version
- **Bug fixes:** Increment patch version (e.g., `1.0.0-dev.2` → `1.0.0-dev.3` or `1.0.0` → `1.0.1`)
- **New features:** Increment minor version (e.g., `1.0.0` → `1.1.0`)
- **Breaking changes:** Increment major version (e.g., `1.0.0` → `2.0.0`)
- **Development releases:** Append or increment `-dev.X` suffix

### How to Bump Version
Edit the `version` field in `pyproject.toml`:
```toml
[project]
name = "midi-diff"
version = "1.0.0-dev.3"  # <-- Update this line
```

**IMPORTANT:** After changing version, always run `poetry build` to ensure build artifacts reflect the new version.

## Development Workflow

1. **Make code changes** in `midi_diff/*.py`
2. **Update CHANGELOG.md** for user-facing changes (see Changelog Requirements below)
3. **Bump version** in `pyproject.toml` if appropriate for the changes
4. **Run Poetry install** if dependencies changed: `poetry install`
5. **Build package**: `poetry build`
6. **Test manually** with MIDI files (no automated tests available)
7. **Verify imports work**: `poetry run python -c "from midi_diff.cli import cli; print('OK')"`

## Changelog Requirements

**CRITICAL:** All PRs with user-facing changes MUST update `CHANGELOG.md` before merging.

### When to Update CHANGELOG.md

Update the changelog for:
- New features or functionality
- Bug fixes affecting user behavior
- Breaking changes or deprecations
- CLI argument/option changes
- Performance improvements
- Security fixes
- Significant documentation changes

### How to Update

1. Edit `CHANGELOG.md` in the repository root
2. Add entries under the `[Unreleased]` section
3. Use appropriate categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
4. Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

### Example Entry

```markdown
## [Unreleased]

### Added
- Support for JSON export format (#42)

### Fixed
- Crash when processing MIDI files with empty tracks (#38)
```

See `CONTRIBUTING.md` for detailed changelog guidelines.

## Important Notes for Agents

- **ALWAYS verify Python 3.13+ is available before attempting `poetry install`**
- **ALWAYS update CHANGELOG.md** when making user-facing changes (new features, bug fixes, breaking changes, etc.)
- **DO NOT commit** `poetry.lock`, `dist/`, or `__pycache__/` (all gitignored)
- **DO NOT modify** Python version requirement in `pyproject.toml` without explicit instruction
- **The CLI has no --help flag** - running without args shows usage
- **No tests exist** - focus on build success and manual verification
- **Import structure:** The package can be imported as `midi_diff` or run as `midi-diff` CLI command
- **Output file safety:** `core.main()` never overwrites files - it auto-increments the filename
- **Velocity is ignored in diffs** - only pitch, start time, and duration matter for comparison
- **Changelog format:** Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) - see `CONTRIBUTING.md` for details

## File Listing

**Root files:**
- `.gitignore` (110 lines)
- `CHANGELOG.md` (Keep a Changelog format)
- `CONTRIBUTING.md` (Contribution guidelines with changelog requirements)
- `LICENSE.md` (MIT License, Inspyre Softworks)
- `README.md` (71 bytes, minimal)
- `pyproject.toml` (411 bytes, project config)

**Package files (midi_diff/):**
- `__init__.py` (27 lines)
- `cli.py` (42 lines)
- `core.py` (104 lines)
- `midi_utils.py` (229 lines)

**Total:** ~400 lines of Python code

---

**Last Updated:** 2026-01-10  
**Validated with:** Python 3.12.3 (with version override), Poetry 2.2.1
