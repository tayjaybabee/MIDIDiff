# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md file to track project changes
- Contribution guidelines (CONTRIBUTING.md) with changelog maintenance requirements
- Changelog maintenance requirements added to agent instructions

### Changed
- Updated documentation to mandate changelog updates for user-facing changes

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

[Unreleased]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.2...HEAD
[1.0.0-dev.2]: https://github.com/tayjaybabee/MIDIDiff/releases/tag/v1.0.0-dev.2
