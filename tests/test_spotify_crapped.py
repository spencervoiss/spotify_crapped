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

def test_filter_by_artists():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(path)
    artists_filter = spotify_crapped.filter_by_artists(lh.listening_history, ["Playboy Manbaby", "yellow book"])
    lh.add_filter(artists_filter)
    assert len(lh.filtered_history) == 7

def test_filter_by_not_skipped():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(path)
    not_skipped_filter = spotify_crapped.filter_by_not_skipped(lh.listening_history)
    lh.add_filter(not_skipped_filter)
    assert len(lh.filtered_history) == 19
    lh.reset_filters()
    assert len(lh.filtered_history) == 22

def test_filter_by_years():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(path)
    years_filter = spotify_crapped.filter_by_years(lh.listening_history, [2024])
    lh.add_filter(years_filter)
    assert len(lh.filtered_history) == 21
    years_filter = spotify_crapped.filter_by_years(lh.listening_history, [2021])
    lh.add_filter(years_filter)
    assert len(lh.filtered_history) == 0