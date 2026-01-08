"""


Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/__init__.py
 

Description:
    

"""
import sys
from midi_utils import extract_notes, notes_to_midi
import mido



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python diff_midi.py fileA.mid fileB.mid diff.mid")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
