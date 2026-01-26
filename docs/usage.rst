Usage Guide
===========

Command-Line Interface
----------------------

MIDIDiff provides several commands and options for working with MIDI files.

Diff Command
~~~~~~~~~~~~

The main functionality - compare two MIDI files:

.. code-block:: bash

   midi-diff diff fileA.mid fileB.mid output.mid

Or with backward compatibility (the ``diff`` subcommand is optional):

.. code-block:: bash

   midi-diff fileA.mid fileB.mid output.mid

Debug Info Command
~~~~~~~~~~~~~~~~~~

Display diagnostic and environment information:

.. code-block:: bash

   midi-diff debug-info

This shows:

* Python version
* MIDIDiff version
* Installation path
* Dependencies and their versions
* System information

Check Updates Command
~~~~~~~~~~~~~~~~~~~~~

Check for available updates from PyPI:

.. code-block:: bash

   midi-diff check-updates

Upgrade Command
~~~~~~~~~~~~~~~

Upgrade midi-diff to the latest version:

.. code-block:: bash

   midi-diff upgrade

To include pre-release versions:

.. code-block:: bash

   midi-diff upgrade --pre

Completion Command
~~~~~~~~~~~~~~~~~~

Generate shell completion scripts for popular shells:

.. code-block:: bash

   midi-diff completion bash        # Bash
   midi-diff completion zsh         # Zsh
   midi-diff completion fish        # Fish
   midi-diff completion powershell  # PowerShell
   midi-diff completion cmd         # Command Prompt (prints doskey helper)

Follow your shell's instructions to load the printed script (e.g., source it or place it in your completions directory).

Version Information
~~~~~~~~~~~~~~~~~~~

Display version and environment info:

.. code-block:: bash

   midi-diff --version
   # or
   midi-diff -V

To include an update check, set the environment variable:

.. code-block:: bash

   MIDIFF_CHECK_UPDATES=1 midi-diff --version

Architecture
------------

CLI Sub-package (v1.0.0+)
~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with version 1.0.0, the CLI has been separated into its own sub-package
(``midi_diff.cli``) to improve separation of concerns and allow the core library
to be used without CLI dependencies.

* **Core library** (``midi_diff``): Contains note extraction, diff logic, and data models.
  Has minimal dependencies (``mido`` only).
* **CLI sub-package** (``midi_diff.cli``): Contains argument parsing, version reporting,
  debug info, and environment checks. Requires ``rich`` for enhanced output.

**Migration note:** If you were importing from ``midi_diff.cli`` in your code, this
continues to work through a backward compatibility shim that will be maintained
through the 1.x release series.

API Stability
-------------

Starting with version 1.0.0, the following API surface is considered stable and
will follow semantic versioning:

* **Core functions**: :func:`midi_diff.core.main`
* **Data models**: :class:`midi_diff.midi_utils.NoteEvent`
* **Utility functions**: :func:`midi_diff.midi_utils.extract_notes`, :func:`midi_diff.midi_utils.notes_to_midi`
* **CLI entry point**: ``midi-diff`` command and :func:`midi_diff.cli.cli` function

Breaking changes to these APIs will result in a major version bump (2.0.0, etc.).
