"""


Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/midi_utils.py
 

Description:
    Utility functions for parsing MIDI files into note events and constructing MIDI files from note events.

"""
from typing import List
import mido


class NoteEvent:
    """
    Simple representation of a note's pitch, start tick, duration, and velocity.
    """
    def __init__(self, pitch: int, start: int, duration: int, velocity: int):
        self.pitch = pitch
        self.start = start
        self.duration = duration
        self.velocity = velocity

    def __eq__(self, other):
        return (
            self.pitch == other.pitch
            and self.start == other.start
            and self.duration == other.duration
        )

    def __hash__(self):
        return hash((self.pitch, self.start, self.duration))

    def __repr__(self):
        return (
            f"Note(p={self.pitch}, start={self.start}, dur={self.duration}, vel={self.velocity})"
        )

def extract_notes(mid: mido.MidiFile) -> List[NoteEvent]:
    """
    Parses a MIDI file and returns a list of NoteEvents.
    """
    notes = []

    for track in mid.tracks:
        ongoing = {}  # key: pitch, value: (start_tick, velocity)
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                ongoing[msg.note] = (tick, msg.velocity)
            elif (msg.type == "note_off") or (
                msg.type == "note_on" and msg.velocity == 0
            ):
                if msg.note in ongoing:
                    start, vel = ongoing.pop(msg.note)
                    duration = tick - start
                    notes.append(NoteEvent(msg.note, start, duration, vel))

    return notes

def notes_to_midi(notes: List[NoteEvent], ticks_per_beat=480) -> mido.MidiFile:
    """
    Constructs a minimal MIDI file containing only the given notes.
    """
    mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # sort events by start time
    events = []
    for note in notes:
        events.append((note.start, mido.Message("note_on", note=note.pitch, velocity=note.velocity)))
        events.append((note.start + note.duration, mido.Message("note_off", note=note.pitch, velocity=0)))

    events.sort(key=lambda e: e[0])

    last_tick = 0
    for tick, msg in events:
        delta = tick - last_tick
        msg.time = int(delta)
        track.append(msg)
        last_tick = tick

    return mid
