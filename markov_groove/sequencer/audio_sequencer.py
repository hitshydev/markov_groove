"""
TODO: Do not use sampler
"""
from typing import Any, Dict, List, Union

import essentia as es
import numpy as np
from matplotlib.ticker import EngFormatter, MultipleLocator
from nptyping import NDArray

from ..audio_file import AudioFile
from ..onset_detector import OnsetAlgorithm, OnsetDetector
from ..sampler import Sampler
from .sequencer import Sequencer


class AudioSequencer(Sequencer):
    """
    TODO: This is part of bla
    """

    pattern: NDArray[float]
    __bpm: int
    __vars: Dict[str, Any]

    # max step amount 16
    def __init__(
        self, pattern: NDArray[float], bpm: int, beats: int = 8, steps: int = 16,
    ) -> None:
        self.pattern = pattern
        self.__bpm = bpm
        self.__vars = {"beats": beats, "steps": steps}
        self.__update_values()

    @classmethod
    def from_file(
        cls,
        file: AudioFile,
        onsets: es.array = None,
        onset_algorithm=OnsetAlgorithm.COMPLEX,
        beats: int = 8,
        steps: int = 16,
    ):
        """
        Create a sequencer from a file.
        TODO
        """
        if onsets is None:
            onsets = OnsetDetector(file, onset_algorithm).onsets
        raise NotImplementedError()

    @classmethod
    def from_sampler(
        cls, sampler: Sampler, bpm: int, beats: int = 8, steps: int = 16,
    ):
        """
        Create a sequencer with an audio sampler by creating the pattern from it.
        """
        sequencer = cls(None, bpm, beats, steps)
        sequencer.__set_pattern_from_sampler(sampler)
        return sequencer

    @property
    def bpm(self) -> int:
        """
        Returns the current bpm of the sequencer.
        """
        return self.__bpm

    @bpm.setter
    def bpm(self, bpm: int) -> None:
        """
        Set the bpm and adjust all related attributes.
        """
        self.__bpm = bpm
        self.__update_values()

    def create_beat(self, *args, sample_rate: int = 44100, **kwargs) -> AudioFile:
        """
        Create a beat from the given samples,
        which have to match the length of occurrences in the pattern.
        """
        samples = args[1] if len(args) > 1 else None
        for key, value in kwargs.items():
            if key == "samples":
                samples = value

        if len(samples) != len(
            [freq for idx, freq in self.pattern if not np.isnan(freq)]
        ):
            raise ValueError("Number of samples does not match with amount of hits!")
        step_length = int(np.round(self.__vars["step_width"] * sample_rate))
        loop_length = int(
            np.round(
                self.__vars["step_amount"] * self.__vars["step_width"] * sample_rate
            )
        )
        zeros = np.zeros(loop_length, dtype=np.float32)
        zeros_step = np.zeros(step_length, dtype=np.float32)
        raw_audio = np.zeros(loop_length, dtype=np.float32)
        sample_index = 0
        for idx, freq in self.pattern:
            if not np.isnan(freq):
                tmp = np.tile(zeros_step, int(idx))
                tmp = np.append(tmp, samples[sample_index])
                tmp = np.append(tmp, zeros)
                raw_audio += tmp[:loop_length]
                sample_index += 1

        return AudioFile(raw_audio, bpm=self.__bpm)

    # mypy: ignore
    @classmethod
    def decode(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decode the pattern of a string and create a sequencer from it.
        """
        # TODO: Estimate beats, steps and bpm
        pattern = np.empty((len(string_pattern), 2), dtype=np.float32)
        for idx, string in enumerate(string_pattern):
            new_idx, freq = string.split(",")
            pattern[idx, 0], pattern[idx, 1] = int(float(new_idx)), np.float32(freq)
        return cls(pattern, bpm, beats, steps)

    def encode(self) -> List[str]:
        """
        Encode the pattern in a string.
        """
        return [f"{idx},{freq}" for idx, freq in self.pattern]

    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str = "+"):
        """
        Visualize the pattern.
        """
        x_length = np.arange(0, len(self.pattern))
        ax_subplot.set(yscale="log")
        formatter = EngFormatter(unit="Hz")
        ax_subplot.yaxis.set_major_formatter(formatter)
        ax_subplot.yaxis.set_minor_formatter(formatter)
        ax_subplot.grid(b=True, which="both")
        ax_subplot.xaxis.set_major_locator(MultipleLocator(base=self.__vars["steps"]))
        values = [value for idx, value in self.pattern]
        return ax_subplot.scatter(x_length, values, color=color, marker=marker)

    def __set_pattern_from_sampler(self, sampler: Sampler) -> None:
        time_line = np.linspace(
            0,
            self.__vars["step_width"] * self.__vars["step_amount"],
            self.__vars["step_amount"] + 1,
        )
        onset_indices = _find_indices(
            sampler.onsets, self.__vars["step_width"], time_line
        )
        self.pattern = np.array(
            [[idx, np.nan] for idx in range(len(time_line))], dtype=np.float32
        )
        for idx, centroid in zip(onset_indices, sampler.samples):
            self.pattern[idx][-1] = centroid

    def __update_values(self) -> None:
        self.__vars["step_width"] = 60 / self.__bpm / self.__vars["steps"]
        self.__vars["step_amount"] = self.__vars["beats"] * self.__vars["steps"]


def _find_indices(
    onsets: es.array, step_width: float, time_line: List[float]
) -> List[int]:
    onset_indices: List[int] = []
    append = onset_indices.append
    onset_iter = iter(onsets)
    onset = next(onset_iter)
    for time_index, time in enumerate(time_line):
        if time - (step_width / 2) <= onset <= time + (step_width / 2):
            append(time_index)
            try:
                onset = next(onset_iter)
            except StopIteration:
                break
    return onset_indices
