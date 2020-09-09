"""
This is a test
"""
from pretty_midi import PrettyMIDI
from markov_groove.sequencer import MidiSequencer


def test_encode_decode():
    mid_seq = MidiSequencer.from_file(PrettyMIDI("audio/rock.mid"))
    encoded = mid_seq.encode()
    decoded = MidiSequencer.decode(encoded)
    for mid_row, decoded_row in zip(mid_seq.pattern, decoded.pattern):
        for mid_note, decoded_note in zip(mid_row, decoded_row):
            if mid_note is None and decoded_note is None:
                assert mid_note is None
                assert decoded_note is None
            else:
                assert mid_note.pitch == decoded_note.pitch
                assert mid_note.start == decoded_note.start
