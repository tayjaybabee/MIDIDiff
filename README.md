# MIDIDiff

MIDIDiff compares two MIDI files and produces a third MIDI file containing the
notes that are present in only one of the inputs. Notes are matched by pitch,
start tick, and duration; velocity differences are ignored.

## Requirements

- Python 3.13+
- `mido` (installed automatically via the project dependencies)

## Installation

### With Poetry (recommended for development)

```shell
poetry install
```

### Build and install locally

```shell
poetry build
pip install dist/*.whl
```

## Usage

The CLI expects two input MIDI files and an output path for the diff:

```shell
midi-diff fileA.mid fileB.mid diff.mid
```

You can also run the module directly:

```shell
python -m midi_diff.cli fileA.mid fileB.mid diff.mid
```

### Output behavior

- If the output file already exists, MIDIDiff will append an incrementing suffix
  (for example, `diff_1.mid`) to avoid overwriting.
- The resulting MIDI file contains only notes that are present in one input but
  not the other.

### Version and environment info

Use `-V` or `--version` to print the installed MIDIDiff version, environment
details, and the result of an update check against PyPI:

```shell
midi-diff --version
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- How to contribute code and documentation
- Changelog update requirements
- Development setup
- Pull request process

All contributions with user-facing changes must update the [CHANGELOG.md](CHANGELOG.md) file.

## How note matching works

Notes are considered identical when they share the same:

- Pitch
- Start tick
- Duration

Velocity is intentionally ignored so that the diff focuses on musical placement.
