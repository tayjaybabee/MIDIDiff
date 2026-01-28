Testing Guide
=============

This guide explains how to set up MIDIDiff for development and testing.

Development Installation
------------------------

Editable Install with Poetry (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Poetry automatically installs the package in editable mode, which means changes
to the source code are immediately reflected without needing to reinstall:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/Inspyre-Softworks/MIDIDiff.git
   cd MIDIDiff
   
   # Install with Poetry (includes dev dependencies)
   poetry install --extras cli
   
   # Run the CLI to verify installation
   poetry run midi-diff --version

Editable Install with pip
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to use pip directly instead of Poetry, you can install the package
in editable mode using the ``-e`` flag:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/Inspyre-Softworks/MIDIDiff.git
   cd MIDIDiff
   
   # Install in editable mode with CLI extras
   pip install -e ".[cli]"
   
   # Run the CLI to verify installation
   midi-diff --version

The ``-e`` flag creates a link to your source code directory instead of copying
files, so any changes you make to the code are immediately available.

**Note:** For pip to work correctly, ensure you have the ``build`` and ``poetry-core``
packages installed:

.. code-block:: bash

   pip install build poetry-core

Running Tests
-------------

Manual Testing
~~~~~~~~~~~~~~

Since this project currently has no automated test suite, testing is performed
manually by running the CLI commands and verifying their output.

Test the main diff functionality:

.. code-block:: bash

   # Create test MIDI files (or use your own)
   # Then run:
   poetry run midi-diff diff fileA.mid fileB.mid output.mid
   
   # Verify the output file was created
   ls -lh output.mid

Test other CLI commands:

.. code-block:: bash

   # Test version command
   poetry run midi-diff --version
   
   # Test help command
   poetry run midi-diff --help
   
   # Test debug info
   poetry run midi-diff debug-info
   
   # Test completion generation
   poetry run midi-diff completion bash
   poetry run midi-diff completion zsh
   poetry run midi-diff completion fish
   poetry run midi-diff completion powershell

Import Testing
~~~~~~~~~~~~~~

Verify that the package can be imported correctly:

.. code-block:: bash

   # Test core module imports
   poetry run python -c "import midi_diff; print('✓ midi_diff')"
   poetry run python -c "from midi_diff.cli import cli; print('✓ midi_diff.cli')"
   poetry run python -c "from midi_diff.core import main; print('✓ midi_diff.core')"
   poetry run python -c "from midi_diff.midi_utils import NoteEvent; print('✓ NoteEvent')"

With editable install, you can modify the source code and immediately re-run
these tests without reinstalling.

Building the Package
--------------------

Build both wheel and source distributions:

.. code-block:: bash

   # With Poetry
   poetry build
   
   # Artifacts will be in dist/
   ls -lh dist/

Install from the built wheel:

.. code-block:: bash

   pip install dist/midi_diff-*.whl

Continuous Integration
----------------------

The project uses GitHub Actions for automated testing on multiple platforms
and Python versions. See ``.github/workflows/test.yml`` for the CI configuration.

The CI workflow:

1. Tests on Ubuntu, Windows, and macOS
2. Tests with Python 3.11, 3.12, and 3.13
3. Installs dependencies with Poetry
4. Builds the package
5. Tests package imports
6. Tests CLI commands (--version, --help, debug-info)

Development Workflow
--------------------

Recommended workflow when developing with editable install:

1. **Make changes** to the source code in ``midi_diff/``

2. **Test immediately** without reinstalling:

   .. code-block:: bash
   
      poetry run midi-diff --version
      # Your changes are already active!

3. **Add features or fix bugs** in the appropriate module:
   
   - Core MIDI logic → ``midi_diff/core.py``
   - MIDI utilities → ``midi_diff/midi_utils.py``
   - CLI interface → ``midi_diff/cli/main.py``
   - Version handling → ``midi_diff/cli/version.py``
   - Documentation → ``midi_diff/cli/docs.py``
   - Completions → ``midi_diff/cli/completions.py``

4. **Verify changes work** by running the affected commands

5. **Update documentation** if adding/changing features

6. **Update CHANGELOG.md** for user-facing changes

7. **Commit changes** when satisfied

Verifying Editable Install
---------------------------

To confirm the package is installed in editable mode:

.. code-block:: bash

   # With Poetry
   poetry run pip list | grep midi-diff
   # Should show the package with the source path
   
   # With pip
   pip list | grep midi-diff
   # Should indicate editable install with package location

You can also check the installation location:

.. code-block:: bash

   # With Poetry
   poetry run python -c "import midi_diff; print(midi_diff.__file__)"
   # Should point to your source directory, not site-packages

Common Issues
-------------

Editable install not working
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If changes to the source code aren't reflected:

1. **Verify editable install:**

   .. code-block:: bash
   
      pip list | grep midi-diff
      # Look for "editable" marker or source path

2. **Check for .pyc files:**

   .. code-block:: bash
   
      find . -name "*.pyc" -delete
      find . -name "__pycache__" -type d -exec rm -rf {} +

3. **Reinstall in editable mode:**

   .. code-block:: bash
   
      poetry install --extras cli
      # or
      pip install -e ".[cli]"

Import errors after changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you get import errors after modifying the package structure:

1. **Reinstall the package:**

   .. code-block:: bash
   
      poetry install --extras cli

2. **Clear Python cache:**

   .. code-block:: bash
   
      find . -type d -name "__pycache__" -exec rm -rf {} +
      find . -type f -name "*.pyc" -delete

Build-system not found error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see warnings about missing build backend when using ``pip install -e .``:

.. code-block:: bash

   # Install build dependencies first
   pip install build poetry-core
   
   # Then install in editable mode
   pip install -e ".[cli]"

Contributing
------------

When contributing code, please:

1. Install in editable mode for development
2. Test your changes manually using the CLI
3. Verify all existing commands still work
4. Update documentation for new features
5. Update CHANGELOG.md for user-facing changes
6. Follow the module separation of concerns (see AGENTS.md)

For more details, see `CONTRIBUTING.md <https://github.com/Inspyre-Softworks/MIDIDiff/blob/main/CONTRIBUTING.md>`_.
