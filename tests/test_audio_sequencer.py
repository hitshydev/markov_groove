"""
This is a test
"""
from pathlib import Path
import numpy as np

from pretty_midi import PrettyMIDI
from markov_groove import AudioFile, AudioSequencer, Sampler


def test_encode_decode():
    audio, bpm = AudioFile.from_file(Path("audio/BL_Beat01_(140BPM).wav"), 140), 140
    sampler = Sampler.from_audio(audio)
    seq = AudioSequencer.from_sampler(sampler, bpm)
    encoded = seq.encode()
    decoded = AudioSequencer.decode(encoded, bpm, 8, 16)
    for seq_tuple, decoded_tuple in zip(seq.pattern, decoded.pattern):
        assert seq_tuple[0] == decoded_tuple[0]
        assert _equal_or_both_nan(seq_tuple[1], decoded_tuple[1])


def _equal_or_both_nan(x, y):
    if np.isnan(x) and np.isnan(y):
        return True
    else:
        return x == y
