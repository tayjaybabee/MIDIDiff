# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.4...v1.0.0
[1.0.0-dev.4]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.3...v1.0.0-dev.4
[1.0.0-dev.3]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.2...v1.0.0-dev.3
[1.0.0-dev.2]: https://github.com/tayjaybabee/MIDIDiff/releases/tag/v1.0.0-dev.2
