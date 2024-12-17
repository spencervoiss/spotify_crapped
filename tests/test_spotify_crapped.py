import pytest
import pathlib
import spotify_crapped.spotify_crapped as spotify_crapped

def test_add_history():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(path)
    assert len(lh.listening_history) == 22
    extra_data_path = pathlib.Path(__file__).parent / "data" / "test_data_2.json"
    lh.add_history(extra_data_path)
    assert len(lh.listening_history) == 25
