"""
CLI commands

"""
import essentia

essentia.log.errorActive = False

from pathlib import Path

import click
from pomegranate import HiddenMarkovModel, DiscreteDistribution
import markov_groove.util as util

from markov_groove.onset_detector import OnsetAlgorithm

# pylint: disable=too-many-arguments
@click.command()
@click.argument(
    "genre_folder", type=click.Path(exists=True, dir_okay=True, readable=True)
)
@click.argument("bpm", default=120)
@click.option(
    "--beats", default=8, type=int, help="Length of the created beat. Defaults to 8."
)
@click.option(
    "--steps", default=16, type=int, help="Resolution of every beat. Defaults to 16."
)
@click.option(
    "--onset",
    default="complex",
    type=str,
    help="The algorithm used for the onset detection. Defaults to complex.",
)
@click.option(
    "--components",
    default=12,
    type=int,
    help="The number of hidden states of the markov model. Defaults to 16.",
)
@click.option(
    "--regex",
    default="*/*.*",
    type=str,
    help="The regex the search for the input files. Defaults to every file in every next folder.",
)
@click.option(
    "--output",
    default=".temp/audio.wav",
    type=click.Path(dir_okay=True, readable=True),
    help="Output path of the exported beat.",
)
@click.option(
    "--include/--no-include",
    default=False,
    help="Include or not include variations of beats. Defaults to not.",
)
def generate(
    genre_folder: str,
    bpm: int,
    beats: int,
    steps: int,
    onset: str,
    components: int,
    regex: str,
    output: str,
    include: bool,
):
    """
    This command generates a new unique beat, based on the audio files in the given input folder.
    """

    audios = util.read_audio_files(include, Path(genre_folder), regex)

    sequences, samples = util.create_knowledge_base(
        audios, OnsetAlgorithm(onset.lower()), beats, steps
    )

    # Create the model
    # sequences = [add_up_ones(seq) for seq in sequences]
    model: HiddenMarkovModel = HiddenMarkovModel.from_samples(
        DiscreteDistribution,
        n_components=components,
        X=sequences,
        algorithm="viterbi",
        verbose=True,
        name="groover",
    )
    # model: MarkovChain = MarkovChain.from_samples(X=sequences)
    # lengths: List[int] = [len(x) for x in sequences]
    sequence = model.sample(length=beats * steps)
    sequence = sequences[0]
    print(sequence)
    # sequence = ones(sequence)
    # print(len(sequence))
    print(
        "BPM: {}, Beats: {}, Steps:{}, Onset Algorithm: {}".format(
            bpm, beats, steps, onset
        )
    )

    # Save the beat
    util.create_beat(sequence, samples, bpm, beats, steps).save(Path(output))


if __name__ == "__main__":
    # Ignore pylint error, because the click module figures it out itself
    # pylint: disable=no-value-for-parameter
    generate()
