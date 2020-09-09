from typing import List, Union

import numpy as np
from nptyping import NDArray
from pretty_midi import Instrument, Note, PrettyMIDI, note_number_to_drum_name
from matplotlib.ticker import FuncFormatter

from ..audio_file import AudioFile
from .sequencer import Sequencer

_VELOCITY: int = 100
_NOTE_DURATION: float = 0.05


class MidiSequencer(Sequencer):
    """
    TODO: This is part of bla
    """

    pattern: NDArray[Note]
    column_sampling: int

    def __init__(self, pattern: NDArray[Note], column_sampling: int = 100):
        self.pattern = pattern
        self.column_sampling = column_sampling

    @classmethod
    def from_file(cls, mid: PrettyMIDI, column_sampling: int = 100):
        """
        TODO: This is part of bla
        """
        drum_track = _find_drum_track(mid)
        # Allocate the array
        pattern = np.empty(
            (128, int(column_sampling * drum_track.get_end_time() + 1)), dtype=np.object
        )
        pattern.fill(None)
        # Add up notes
        for note in drum_track.notes:
            pattern[note.pitch, int(note.start * column_sampling)] = note
        return cls(pattern, column_sampling)

    def create_beat(self, *args, sample_rate: int = 44100, **kwargs) -> AudioFile:
        """
        Create a beat from the pattern in the sequencer.
        """
        bpm = args[1] if len(args) > 1 else 120
        for key, value in kwargs.items():
            if key == "bpm":
                bpm = value

        mid = PrettyMIDI(initial_tempo=bpm)
        drum_track = Instrument(program=0, is_drum=True, name="drums")
        mid.instruments.append(drum_track)
        for row in self.pattern:
            for value in row:
                if value is not None:
                    drum_track.notes.append(value)
        return AudioFile(
            np.array(mid.fluidsynth(fs=sample_rate), dtype=np.float32), bpm, sample_rate
        )

    @classmethod
    def decode(cls, string_pattern: List[str]):
        """
        Decode the pattern of a string list and create a sequencer from it.
        """
        # TODO: Estimate column_sampling
        column_sampling: int = 100
        # Allocate the array
        pattern = np.empty((128, len(string_pattern)), dtype=np.object)
        pattern.fill(None)
        for string in string_pattern:
            notes = _string_to_notes(string)
            for note in notes:
                pattern[note.pitch, int(note.start * column_sampling)] = note

        return cls(pattern, column_sampling)

    def encode(self) -> List[str]:
        """
        Encode the pattern in a list of strings.
        """
        string_list = ["" for _ in range(self.pattern.shape[-1])]
        for row in self.pattern:
            for idx, note in enumerate(row):
                if note is not None:
                    string_list[idx] += f"{note.pitch},{note.start};"
        return string_list

    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str = "2"):
        """
        Visualize the pattern.
        """
        x_length = np.arange(0, self.pattern.shape[-1])
        for note_row in self.pattern:
            values = [note.pitch if note is not None else np.nan for note in note_row]
            ax_subplot.scatter(x_length, values, color=color, marker=marker)
        ax_subplot.yaxis.set_major_formatter(
            FuncFormatter(lambda tick, pos: note_number_to_drum_name(tick))
        )
        return ax_subplot


def _find_drum_track(mid: PrettyMIDI) -> Instrument:
    """
    Gets the first occurrence of a drum track in a PrettyMIDI file.
    """
    for instrument in mid.instruments:
        if instrument.is_drum:
            return instrument
    raise ValueError("No drum track found!")


def _string_to_notes(string: str) -> List[Note]:
    arguments = string.split(";")
    return [_string_to_note(x) for x in arguments if x]


def _string_to_note(string: str) -> Note:
    arguments = string.split(",")
    pitch, start = int(arguments[0]), float(arguments[1])
    return Note(_VELOCITY, pitch, start, start + _NOTE_DURATION)
