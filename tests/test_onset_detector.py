"""
This is a test
"""
from pathlib import Path
from typing import List

from markov_groove.audio_file import AudioFile
from markov_groove.onset_detector import OnsetAlgorithm, OnsetDetector

# Predefined estimated onsets of the hfc algo in seconds
ONSETS_HFC: List[float] = [
    0.01160998,
    0.20897959,
    0.42956915,
    0.6501587,
    0.8591383,
    1.0681179,
    1.2887075,
    1.4976871,
    1.6253968,
    1.7298867,
    1.8459864,
    1.9272562,
    2.1478457,
    2.3568254,
    2.4729252,
    2.589025,
    2.6935148,
    2.7863946,
    3.0069842,
    3.157914,
    3.2159636,
    3.3320634,
]


def test_hfc():
    file: AudioFile = AudioFile.from_file(
        Path("audio/BL_Beat01_(140BPM).wav").absolute()
    )
    onset: OnsetDetector = OnsetDetector(file, OnsetAlgorithm.HFC)
    for i, stamp in enumerate(ONSETS_HFC):
        assert int(onset.onsets[i]) == int(stamp)
