"""
TODO: This is part of bla
"""
from typing import Dict, List

import essentia as es
import essentia.standard as estd
import numpy as np
from more_itertools import pairwise

from .audio_file import AudioFile
from .onset_detector import OnsetAlgorithm, OnsetDetector, Window


class Sampler:
    """
    This class creates samples from the onset frames.
    """

    samples: Dict[float, es.array]
    onsets: List[float]
    __file: AudioFile

    def __init__(
        self, file: AudioFile, onsets: es.array, samples: Dict[float, es.array],
    ):
        self.__file = file
        self.onsets = onsets
        self.samples = samples

    @classmethod
    def from_audio(
        cls,
        audio: AudioFile,
        windowfnc: Window = Window.HANN,
        onsets: es.array = None,
        onset_algorithm: OnsetAlgorithm = OnsetAlgorithm.COMPLEX,
        use_max: bool = False,
    ):
        """
        Creates a sampler from a given AudioFile.
        """
        if onsets is None:
            onsets = OnsetDetector(audio, onset_algorithm).onsets

        onset_indices = (int(i) for i in onsets * audio.sample_rate)
        spectral_centroids = lambda sample: _key_fnc(
            sample, int(audio.sample_rate / 2), windowfnc, use_max
        )

        frames = (
            np.append(
                audio.audio[index:next_index],
                np.zeros(len(audio.audio[index:next_index]), dtype=np.float32),
            )
            for index, next_index in pairwise(onset_indices)
        )
        samples = {spectral_centroids(sample): sample for sample in frames}

        return Sampler(audio, onsets, samples)

    @property
    def sample_rate(self) -> int:
        """
        Return the sampling rate.
        """
        return self.__file.sample_rate


def _key_fnc(
    sample: es.array, frequency_rate: int, windowfnc: Window, use_max: bool = False
) -> float:
    """
    This function computes the key function,
    which in return calculates the keys for the [this.samples] map.
    To calculate the spectral centroid,
    the frequency_rate should be equal to the half of the samplerate.
    """
    if use_max:
        return _get_max(
            sample,
            estd.Spectrum(),
            estd.Windowing(size=len(sample), type=windowfnc.value),
        )
    return _get_centroid(
        sample,
        estd.Centroid(range=frequency_rate),
        estd.Spectrum(),
        estd.Windowing(size=len(sample), type=windowfnc.value),
    )


def _get_centroid(sample: es.array, centroid, spectrum, window) -> float:
    """
    Return the centroid of an array.
    It can be used to compute the spectral or the temporal centroid.
    For more information view: https://essentia.upf.edu/reference/std_Centroid.html.
    """
    return centroid(spectrum(window(sample)))


def _get_max(sample: es.array, spectrum, window) -> float:
    """
    This function could be used as another key, for the get_key closure.
    """
    print(spectrum(window(sample)))
    raise NotImplementedError()
    return np.argmax(spectrum(window(sample)))
