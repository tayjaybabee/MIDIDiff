.. MIDIDiff documentation master file, created by
   sphinx-quickstart on Fri Jan 23 14:49:21 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MIDIDiff Documentation
======================

MIDIDiff compares two MIDI files and produces a third MIDI file containing the
notes that are present in only one of the inputs. Notes are matched by pitch,
start tick, and duration; velocity differences are ignored.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   usage
   shell-completions
   testing
   api
   contributing

Features
--------

* Compare two MIDI files and extract differences
* Command-line interface with rich formatting
* Programmatic API for Python integration
* Automatic output file collision avoidance
* Version and environment information commands

Quick Example
-------------

Command-line usage:

.. code-block:: bash

   midi-diff fileA.mid fileB.mid output.mid

Programmatic usage:

.. code-block:: python

   from midi_diff.core import main

   # Compare two MIDI files and save the diff
   main('fileA.mid', 'fileB.mid', 'diff.mid')

Requirements
------------

* Python 3.11+
* mido (installed automatically)
* rich (optional, for enhanced CLI output)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`