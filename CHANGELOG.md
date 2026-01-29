# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-01-29

### Added
- Added `install-completions` subcommand to generate and install shell completions for the current shell (with optional `--shell` override).
- Completion scripts now include option/flag completions for subcommands.

## [1.0.8] - 2026-01-28

### Fixed
- Fixed `upgrade` command to use exact version specifier (`==`) when upgrading via pip, ensuring the package is properly upgraded even when pip incorrectly reports "Requirement already satisfied".

## [1.0.7] - 2026-01-28

### Fixed
- Fixed `NameError` in bash completion script generation caused by unescaped curly braces in f-string for bash variables (`COMP_WORDS`, `COMP_CWORD`).

### Added
- Comprehensive shell completions documentation (`docs/shell-completions.rst`) with detailed installation instructions for bash, zsh, fish, PowerShell, and cmd.
- Comprehensive testing and development guide (`docs/testing.rst`) with detailed instructions for editable installs using both Poetry and pip.
- `[build-system]` section in pyproject.toml to properly configure poetry-core as the build backend.
- Updated README.md, CONTRIBUTING.md, and usage.rst with editable install instructions and references to new documentation.

### Changed
- Installation documentation now emphasizes editable install (`-e` flag) for development workflow.
- README.md now features a dedicated "For Development" section at the top of the Installation guide.
- Standardized on `poetry install --extras cli` as the primary development command across all documentation, with pip alternatives clearly marked as secondary.
- Improved consistency in editable install guidance throughout README.md, CONTRIBUTING.md, and docs/testing.rst.

## [1.0.6] - 2026-01-27

### Added
- `completion` subcommand to generate shell completion scripts (bash, zsh, fish, PowerShell, cmd).

## [1.0.5] - 2026-01-26

### Fixed
- Windows upgrade command now retries with `--user` when a file lock (`WinError 32`) blocks overwriting the `midi-diff.exe` shim, avoiding upgrade failures.

## [1.0.4] - 2026-01-26

### Added
- Sphinx documentation with autodoc, napoleon, and Read the Docs theme
  - Comprehensive API documentation for all modules and classes
  - Installation, quickstart, usage, and contributing guides
  - Code-blocks with syntax highlighting
  - Cross-references and intersphinx support for Python and mido documentation
  - `.readthedocs.yaml` configuration for automatic RTD builds
- `docs` subcommand to open MIDIDiff documentation (https://mididiff.readthedocs.io/en/latest/) in the user's default web browser
  - Opens documentation in default browser
  - Graceful error handling with manual URL fallback
  - Follows module separation pattern with dedicated `cli/docs.py` module
- AI assistant instruction files for better code quality and consistency
  - Updated AGENTS.md with module separation of concerns guidelines
  - Updated .github/copilot-instructions.md with module separation guidelines
  - New SOURCERY.md with comprehensive Sourcery AI instructions
  - New .sourcery.yaml configuration file
- Status badges to README.md
  - PyPI version badge
  - Python versions badge (3.11, 3.12, 3.13)
  - MIT license badge
  - GitHub Actions test status badge
  - Read the Docs documentation status badge

### Changed
- Updated README.md Python version requirement from 3.13+ to 3.11+ to match pyproject.toml
- Fixed pip install command in README.md to use proper wheel filename pattern (`midi_diff-*.whl`)
- Updated CLI module path in README.md to include `diff` subcommand
- Moved module entry point logic from `__init__.py` to dedicated `__main__.py` following Python conventions

### Fixed
- README.md pip install command with wildcard inside quotes (should expand glob first)
- pyproject.toml: Changed `[dependency-groups]` to `[tool.poetry.group.dev.dependencies]` for proper Poetry recognition
- docs/usage.rst: Corrected environment variable name from `MIDI_DIFF_CHECK_UPDATES` to `MIDIFF_CHECK_UPDATES`
- Running `python -m midi_diff` now dispatches to the CLI entry point instead of printing the legacy usage string

## [1.0.2] - 2026-01-21

### Added
- `check-updates` subcommand to explicitly check for available updates from PyPI
- `upgrade` subcommand to upgrade midi-diff to the latest version using pip
- `--pre` flag for `upgrade` subcommand to include pre-release versions
- CI/CD workflow (`.github/workflows/test.yml`) for automated testing across Python 3.11/3.12/3.13 on Ubuntu/Windows/macOS
  - Validates package build, imports, and CLI commands (`--version`, `--help`, `debug-info`)
  - Runs on push/PR to `master`, `main`, and `develop` branches
  - Uses `fail-fast: false` to ensure all platform/version combinations are tested

### Fixed
- Windows CI build failures by switching from `snok/install-poetry` action to direct `pip install poetry` approach for better cross-platform compatibility

## [1.0.1] - 2026-01-21

### Changed
- Replaced dynamic subcommand/flag extraction with explicit `KNOWN_COMMANDS` and `KNOWN_FLAGS` constants for better maintainability
- Introduced individual command and flag constants (`COMMAND_DIFF`, `COMMAND_DEBUG_INFO`, `FLAG_VERSION_SHORT`, etc.) as single source of truth, referenced by both `build_parser()` and backward compatibility logic to prevent drift
- `run_cli()` now accepts optional `argv` parameter (type-annotated as `Sequence[str] | None`) for improved testability
- CLI argument parsing no longer mutates `sys.argv`
- Added Python 3.12 and 3.13 classifiers to PyPI metadata to match declared version constraint

### Fixed
- Release workflow now triggers on the default `master` branch
- Version flag (`-V`/`--version`) now checks for updates when `MIDIFF_CHECK_UPDATES` environment variable is set, even when Rich library is not installed

### Removed
- `midi_diff/cli.py` backward compatibility shim (conflicts with new package structure)
- `_get_known_subcommands_and_flags()` function that relied on private argparse APIs
- Redundant `if __name__ == "__main__":` block from `midi_diff/cli/__init__.py`

## [1.0.0] - 2026-01-14

### Added
- CLI sub-package (`midi_diff.cli`) with dedicated modules for version info, debug info, and argument parsing
- Optional CLI dependency group for `rich` library, allowing core library use without CLI dependencies
- Fallback plain-text output when `rich` is not installed
- `debug-info` subcommand for displaying comprehensive diagnostic information
- Programmatic API examples in README
- API stability guarantees for 1.x release series
- Migration notes for CLI sub-package restructure

### Changed
- **Breaking (internal)**: Separated CLI into dedicated sub-package (`midi_diff/cli/`) from single `cli.py` module
- CLI dependencies (`rich`) moved to optional extras group `[cli]` in `pyproject.toml`
- Core library (`midi_diff`) now has minimal dependencies (only `mido`)
- Backward compatibility maintained through shim in `midi_diff/cli.py` for existing imports

### Fixed
- None

## [1.0.0-dev.4] - 2026-01-14

### Added
- CHANGELOG.md file to track project changes
- Contribution guidelines (CONTRIBUTING.md) with changelog maintenance requirements
- Pull request template with changelog update requirements
- Issue templates for bug reports and feature requests
- `rich` library as a dependency for enhanced terminal output
- Colorized and formatted version output (`-V`/`--version`) using rich panels and tables
- `debug-info` subcommand for displaying comprehensive diagnostic information in Rich Markdown format
- Roadmap documenting the planned CLI sub-package separation and 1.0.0 release steps

### Changed
- Updated documentation to mandate changelog updates for user-facing changes
- Consolidated changelog guidance to CONTRIBUTING.md with references from AGENTS.md and copilot-instructions.md to reduce duplication
- Simplified PR template to have single changelog checklist item instead of duplicate entries
- Version info display now uses rich formatting with colored table and panel layout
- CLI refactored to use subcommand structure (argparse subparsers) with `diff` and `debug-info` subcommands
- `diff` subcommand is now the default when no subcommand is specified, maintaining backward compatibility with original CLI usage

## [1.0.0-dev.3] - 2026-01-12

### Changed
- Refactored CLI version lookup to reuse shared metadata retrieval and remove duplication

## [1.0.0-dev.2] - 2026-01-10

### Added
- Command-line tool for comparing MIDI files and generating diff files
- Support for note matching by pitch, start tick, and duration (velocity ignored)
- Automatic output file name incrementing to prevent overwrites
- Version flag (`-V`/`--version`) with environment details and PyPI update check
- Poetry-based build system with Python 3.13+ requirement
- Extract notes from MIDI files using `mido` library
- Set-based note comparison for efficient diffing
- Output only notes present in one file but not the other
- Immutable `NoteEvent` dataclass with MIDI bounds validation

[Unreleased]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.4...HEAD
[1.0.4]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.4...v1.0.0
[1.0.0-dev.4]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.3...v1.0.0-dev.4
[1.0.0-dev.3]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.2...v1.0.0-dev.3
[1.0.0-dev.2]: https://github.com/tayjaybabee/MIDIDiff/releases/tag/v1.0.0-dev.2
