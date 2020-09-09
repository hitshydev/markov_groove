"""
TODO: This is part of bla
"""
from abc import ABC, abstractmethod
from typing import Any, List, Union

from nptyping import NDArray

from markov_groove.audio_file import AudioFile


class Sequencer(ABC):
    """
    TODO: This is part of bla
    """

    pattern: NDArray[Any]

    @abstractmethod
    def create_beat(self, *args, sample_rate: int = 44100, **kwargs) -> AudioFile:
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
    def decode(cls, string_pattern: List[str]):
        """
        Decode the pattern of a string and create a sequencer from it.
        """

    @abstractmethod
    def encode(self) -> List[str]:
        """
        Encode the pattern in a string.
        """
