# MIDIDiff Roadmap

This document captures the near-term plan to separate the CLI into its own
sub-package (improving separation of concerns) and to prepare for the 1.0.0
release.

## CLI Sub-package Separation Plan

**Goal:** Isolate CLI concerns from the core library so that the Python package
exposes a clean API while the CLI can evolve independently.

### Proposed structure
- Keep `midi_diff` as the core library (note extraction, diff logic, data
  models).
- Evolve the existing `midi_diff.cli` module into a dedicated CLI sub-package
  (for example, `midi_diff/cli/__init__.py` and `midi_diff/cli/main.py`) that
  contains:
  - Argument parsing, version/debug info rendering, and environment checks.
  - Entry point definition (`midi-diff = "midi_diff.cli:cli"`), keeping the
    existing convention of a hyphenated distribution/CLI name (`midi-diff`)
    and underscored package/import name (`midi_diff`).
  - Optional CLI-only dependencies (e.g., `rich`) declared separately so the
    core library remains lightweight. Today `rich` is still listed as a core
    dependency in `pyproject.toml`; as part of this separation it will be
    moved into a dedicated CLI extras group (for example
    `[project.optional-dependencies.cli]`).
- Provide a compatibility shim in `midi_diff/cli.py` (or equivalent) that
  delegates to the new internal CLI structure to avoid breaking existing
  imports and the module entry point (`python -m midi_diff.cli`).

### Execution steps
1. Create the new CLI sub-package with a minimal `main.py` that wires the parser
   to the existing `core.main` function.
2. Move CLI-only helpers (version reporting, debug info, update checks) into the
   new package.
3. Update `pyproject.toml` to point the console script at the new package and
   split dependencies so CLI extras (Poetry optional dependency groups such as
   `[project.optional-dependencies]` / `[tool.poetry.extras]`) do not burden
   library consumers.
4. Add focused smoke coverage (CLI invocation and debug-info path) once the new
   package is in place.
5. Document the new layout in `README.md` and migration notes, ensuring the
   compatibility shim remains through 1.x.

## 1.0.0 Release Plan

**Goal:** Ship a stable 1.0.0 that locks in the core API and CLI surface.

### Checklist
1. Finalize CLI split (above) and confirm backwards compatibility for `midi-diff`
   entry point and `python -m midi_diff.cli`.
2. Freeze public API for the core library (note model, diff function signatures)
   and document supported behaviors (e.g., velocity ignored).
3. Audit dependencies and metadata:
   - Pin minimum versions that are validated.
   - Ensure CLI-only dependencies are optional or scoped to extras.
4. Add or update smoke tests (or manual checklists) covering:
   - CLI diff path,
   - Debug-info output,
   - Version flag,
   - Output file safety (no overwrite).
5. Refresh documentation:
   - Update README with new structure and usage examples.
   - Add a short migration note for the CLI sub-package move.
6. Update `CHANGELOG.md` with a 1.0.0 section summarizing finalized features and
   the CLI separation.
7. Bump version in `pyproject.toml` to `1.0.0`, build artifacts with Poetry, and
   publish release/tag.
