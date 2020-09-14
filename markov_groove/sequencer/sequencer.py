"""
TODO: This is part of bla
"""
from abc import ABC, abstractmethod
from typing import Any, List, Union, Final, Dict

from nptyping import NDArray, Float32

from markov_groove.audio_file import AudioFile


class Sequencer(ABC):
    """
    A sequencer can be initalized
    """

    # pattern: NDArray[Any]
    # bpm: int
    # beats: int
    # steps: int

    @abstractmethod
    def create_beat(
        self, samples: Dict[float, NDArray[Float32]] = None, sample_rate: int = 44100,
    ) -> AudioFile:
        """
        Create a beat from the pattern in the sequencer.
        This method requires different parameters for every implementation of Sequencer.
        """

    @abstractmethod
    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str):
        """
        Visualize the pattern.
        """

    @classmethod
    @abstractmethod
    def decode(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decode the pattern of a string and create a sequencer from it.
        """

    @abstractmethod
    def encode(self) -> List[str]:
        """
        Encode the pattern in a string.
        """
