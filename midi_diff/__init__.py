"""


Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/__init__.py
 

Description:
    

"""
from __future__ import annotations

from midi_diff.midi_utils import extract_notes, notes_to_midi


if __name__ == "__main__":
    from midi_diff.cli import cli

    cli()
