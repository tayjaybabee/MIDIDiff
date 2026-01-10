"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/core.py
 

Description:
    Core functionality for comparing two MIDI files and generating a diff MIDI file.

"""
import contextlib
import mido
from midi_diff.midi_utils import extract_notes, notes_to_midi
from typing import Union
from pathlib import Path


def _determine_out_path(out_file: Union[str, Path]) -> Path:
    """
    Determine the final output path for a MIDI diff file. Ensure the path does not overwrite existing files.

    Parameters:
        out_file (str | pathlib.Path):
            Desired output location for the MIDI diff file.

    Returns:
        pathlib.Path:
            A filesystem path that is safe to write to without overwriting an existing file.
    """
    out_path = Path(out_file)
    parent = out_path.parent or Path(".")

    with contextlib.suppress(Exception):
        parent.mkdir(parents=True, exist_ok=True)

    stem = out_path.stem
    suffix = out_path.suffix or ".mid"
    candidate = out_path

    i = 1

    while candidate.exists():
        candidate = parent / f"{stem}_{i}{suffix}"
        i += 1

    return candidate


def main(file_a: Union[str, Path], file_b: Union[str, Path], out_file: Union[str, Path]) -> None:
    """
    Main function to compute the diff between two MIDI files and save the result.

    Parameters:
        file_a (str | pathlib.Path):
            Path to the first MIDI file.

        file_b (str | pathlib.Path):
            Path to the second MIDI file.

        out_file (str | pathlib.Path):
            Path to save the output diff MIDI file. Existing files will be
            avoided by incrementing the filename.
    """
    file_a = Path(file_a)
    file_b = Path(file_b)

    if not file_a.exists():
        print(f"Input file missing: {file_a}")
        return
    if not file_b.exists():
        print(f"Input file missing: {file_b}")
        return

    try:
        mid_a = mido.MidiFile(str(file_a))
        mid_b = mido.MidiFile(str(file_b))
    except Exception as e:
        print(f"Failed to load MIDI files: {e}")
        return

    notes_a = set(extract_notes(mid_a))
    notes_b = set(extract_notes(mid_b))

    only_in_a = notes_a - notes_b
    only_in_b = notes_b - notes_a

    print(f"Notes only in A: {len(only_in_a)}")
    print(f"Notes only in B: {len(only_in_b)}")

    diff_notes = list(only_in_a.union(only_in_b))

    out_path = _determine_out_path(out_file)
    diff_mid = notes_to_midi(diff_notes, ticks_per_beat=mid_a.ticks_per_beat)
    try:
        diff_mid.save(str(out_path))
    except Exception as e:
        print(f"Failed to save diff MIDI: {e}")
        return

    print(f"Saved diff MIDI → {out_path}")