# Contributing to MIDIDiff

Thank you for your interest in contributing to MIDIDiff! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Changelog Requirements](#changelog-requirements)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

Contributions are welcome in the following forms:
- Bug reports and feature requests via GitHub Issues
- Code contributions via Pull Requests
- Documentation improvements
- Bug fixes and enhancements

## Changelog Requirements

**All pull requests with user-facing changes MUST update the CHANGELOG.md file.**

### When to Update the Changelog

Update the changelog when your PR includes:
- New features or functionality
- Bug fixes that affect user behavior
- Breaking changes or deprecations
- Changes to CLI arguments or options
- Performance improvements
- Security fixes
- Documentation changes that significantly affect usage

### When NOT to Update the Changelog

You may skip changelog updates for:
- Internal refactoring that doesn't change behavior
- Test-only changes
- Code comments or minor documentation typos
- Build/CI configuration changes (unless they affect users)

### How to Update the Changelog

1. **Edit CHANGELOG.md** in the repository root
2. **Add your changes under the `[Unreleased]` section**
3. **Use the appropriate category:**
   - `Added` - New features
   - `Changed` - Changes to existing functionality
   - `Deprecated` - Soon-to-be removed features
   - `Removed` - Removed features
   - `Fixed` - Bug fixes
   - `Security` - Security fixes

### Changelog Entry Format

Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

```markdown
## [Unreleased]

### Added
- New feature description in present tense

### Fixed
- Bug fix description referencing issue number (#123)
```

### Examples

Good changelog entries:
```markdown
### Added
- Support for exporting diff files in JSON format (#42)
- New `--ignore-velocity` flag to exclude velocity from comparison

### Fixed
- Fixed crash when processing MIDI files with empty tracks (#38)
- Corrected tempo handling in multi-track MIDI files

### Changed
- Improved performance of note comparison algorithm by 40%
```

Poor changelog entries:
```markdown
### Changed
- stuff
- Fixed things
- Updated code
```

## Development Setup

### Requirements
- Python 3.13+
- Poetry for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tayjaybabee/MIDIDiff.git
   cd MIDIDiff
   ```

2. Install dependencies in editable mode:
   ```bash
   poetry install --extras cli
   ```
   
   This installs the package in editable/development mode, meaning changes to the
   source code are immediately reflected without needing to reinstall.
   
   **Alternative (using pip):**
   ```bash
   pip install -e ".[cli]"
   ```
   
   The `-e` flag ensures an editable install, which is essential for development.

3. Verify installation:
   ```bash
   poetry run midi-diff --version
   ```

**Important:** Always use an editable install (`poetry install --extras cli` or `pip install -e ".[cli]"`) when developing,
so you can test changes immediately without rebuilding/reinstalling the package.

### Building

Build the package locally:
```bash
poetry build
```

This creates wheel and source distributions in the `dist/` directory.

## Submitting Changes

### Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the code style of the project
3. **Update CHANGELOG.md** if your changes are user-facing (see above)
4. **Test your changes** manually with MIDI files
5. **Commit your changes** with clear, descriptive commit messages
6. **Push to your fork** and submit a pull request

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title (e.g., "Add JSON export support" not "Update code")
- **Description**: Explain what changes you made and why
- **Changelog**: Confirm you've updated CHANGELOG.md if appropriate
- **Testing**: Describe how you tested your changes
- **Related Issues**: Reference any related issues (e.g., "Fixes #42")

### Commit Message Format

Use clear, descriptive commit messages:
- Start with a verb in imperative mood (Add, Fix, Update, Remove)
- Keep the first line under 72 characters
- Add additional details in the body if needed

Good examples:
```
Add support for JSON export format

Fix crash when processing empty MIDI tracks (#38)

Update documentation for new --ignore-velocity flag
```

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use type hints for function parameters and return values
- Include docstrings for public functions and classes
- Use descriptive variable and function names
- Keep functions focused and single-purpose

## Questions?

If you have questions about contributing, please open an issue with the "question" label.

## License

By contributing to MIDIDiff, you agree that your contributions will be licensed under the same MIT License that covers the project.
