"""
This is a test
"""
from pathlib import Path

import numpy as np

from markov_groove.audio_file import AudioFile


def test_check_bpm():
    for i in range(1, 6):
        file: AudioFile = AudioFile.from_file(
            Path("audio/BL_Beat0{0}_(140BPM).wav".format(i)).absolute()
        )
        assert np.round(file.check_bpm()) == 140
