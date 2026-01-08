"""


Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli.py
 

Description:
    Command-line interface for MIDIDiff to compare two MIDI files and output their differences.

"""
import sys
from midi_diff.core import main


def cli() -> None:
    """
    Command-line interface for MIDIDiff.

    Usage:
        python -m midi_diff.cli fileA.mid fileB.mid diff.mid

    """
    if len(sys.argv) != 4:
        print("Usage: python -m midi_diff.cli fileA.mid fileB.mid diff.mid")
    else:
        file_a = sys.argv[1]
        file_b = sys.argv[2]
        out_file = sys.argv[3]
        main(file_a, file_b, out_file)


if __name__ == "__main__":
    cli()

