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

import sys

from midi_diff.midi_utils import extract_notes, notes_to_midi


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python diff_midi.py fileA.mid fileB.mid diff.mid")
    else:
        from midi_diff.core import main

        main(sys.argv[1], sys.argv[2], sys.argv[3])
