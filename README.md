<p align="center">
    <img alt="mg_logo" src="mg.svg"/>
</p>

<h1 align="center">Markov Groove</h1> 

<p align="center">
    <a title="AGPLv3 License" href="https://choosealicense.com/licenses/agpl-3.0/">
      <img alt="License: MIT" src="https://img.shields.io/badge/LICENSE-MIT-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge"">
    </a>
    <a href="https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb#scrollTo=8QAWNjizy_3O">
        <img alt="Open In Colab" src="https://img.shields.io/static/v1?label=Notebook&message=Open%20in%20Colab&color=yellow&style=for-the-badge"">
    </a>
</p>

MarkovGroove is a small framework, that uses essentia and PrettyMIDI to convert audio files
into sequencers that can later be used for machine learning tasks. The library got its name
from the mathmatician Andrey Markov, since it was designed to be used with HiddenMarkovModels.
It is part of my bachelor thesis so please cite, if you are using this in a scientific context.

To use the framework in your project or notebooks just import markov_groove:

    import markov_groove as mg
    # Read a mid file
    project.do_stuff()
    # Create a sequencer from it
    project.do_stuff()
    # Visualize the pattern
    project.do_stuff()

There are also some more examples and tutorials under notebooks!

## Features

* Read Audio files
* Read Midi files
* Create step sequencer from audio files
* Extract Samples from onset locations

## Install prerequisites
Some libraries are needed prior before using.

### Essentia
    sudo apt-get install build-essential libeigen3-dev libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six

    sudo apt-get install python3-dev python3-numpy-dev python3-numpy python3-yaml

### Pomegranate

    sudo apt-get install gcc libpq-dev -y 
    sudo apt-get install python-dev  python-pip -y  
    sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y  
    python3 -m pip install wheel

### FluidSynth
    sudo apt-get install fluidsynth
