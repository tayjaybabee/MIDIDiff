"""


Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/core.py
 

Description:
    

"""
import mido
from midi_utils import extract_notes, notes_to_midi


def main(file_a: str, file_b: str, out_file: str):
    """
    Main function to compute the diff between two MIDI files and save the result.

    Parameters:
        file_a (str):
            Path to the first MIDI file.

        file_b (str):
            Path to the second MIDI file.

        out_file (str):
            Path to save the output diff MIDI file.

    Returns:
        None
    """

    # load
    mid_a = mido.MidiFile(file_a)
    mid_b = mido.MidiFile(file_b)

    notes_a = set(extract_notes(mid_a))
    notes_b = set(extract_notes(mid_b))

    # compute diffs
    only_in_a = notes_a - notes_b
    only_in_b = notes_b - notes_a

    print(f"Notes only in A: {len(only_in_a)}")
    print(f"Notes only in B: {len(only_in_b)}")

    # combine or choose direction
    diff_notes = list(only_in_a.union(only_in_b))

    # output
    diff_mid = notes_to_midi(diff_notes, ticks_per_beat=mid_a.ticks_per_beat)
    diff_mid.save(out_file)
    print(f"Saved diff MIDI → {out_file}")
