import pathlib

import pandas as pd
import pytest

import spotify_crapped.spotify_crapped as spotify_crapped


# ███████ ██ ██   ██ ████████ ██    ██ ██████  ███████ ███████
# ██      ██  ██ ██     ██    ██    ██ ██   ██ ██      ██
# █████   ██   ███      ██    ██    ██ ██████  █████   ███████
# ██      ██  ██ ██     ██    ██    ██ ██   ██ ██           ██
# ██      ██ ██   ██    ██     ██████  ██   ██ ███████ ███████


@pytest.fixture
def mock_dirty_playlist():
    """Creates a mock playlist for testing playlist cleaning functions"""
    return pd.DataFrame(
        [
            {
                "Track Name": "track_1",
                "Artist Name(s)": "playlist_artist_1",
            },
            {
                "Track Name": "playlist_track_2",
                "Artist Name(s)": "playlist_artist_2, secondary_artist",
            },
        ]
    )


@pytest.fixture
def mock_clean_playlist():
    """Creates a mock playlist for filtering from listening history"""
    return pd.DataFrame(
        [
            {
                "master_metadata_track_name": "track_1",
                "master_metadata_album_artist_name": "playlist_artist_1",
            },
            {
                "master_metadata_track_name": "playlist_track_2",
                "master_metadata_album_artist_name": "playlist_artist_2",
            },
        ]
    )


@pytest.fixture
def mock_listening_history():
    """Create a short mock listening history for testing purposes"""
    return pd.DataFrame(
        [
            {
                "ts": "2024-10-30T07:00:00Z",
                "master_metadata_track_name": "track_1",
                "master_metadata_album_artist_name": "artist_1",
                "master_metadata_album_album_name": "album_1",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-08-11T18:15:02Z",
                "master_metadata_track_name": "track_2",
                "master_metadata_album_artist_name": "artist_2",
                "master_metadata_album_album_name": "album_2",
                "skipped": False,
                "ms_played": 10,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_3",
                "master_metadata_album_artist_name": "artist_1",
                "master_metadata_album_album_name": "album_1",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_4",
                "master_metadata_album_artist_name": "artist_3",
                "master_metadata_album_album_name": "album_3",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_1",
                "master_metadata_album_artist_name": "artist_3",
                "master_metadata_album_album_name": "album_3",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_4",
                "master_metadata_album_artist_name": "artist_3",
                "master_metadata_album_album_name": "album_3",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2023-09-11T23:30:41Z",
                "master_metadata_track_name": "track_5",
                "master_metadata_album_artist_name": "artist_2",
                "master_metadata_album_album_name": "album_2",
                "skipped": False,
                "ms_played": 10,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_6",
                "master_metadata_album_artist_name": "artist_1",
                "master_metadata_album_album_name": "album_4",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_7",
                "master_metadata_album_artist_name": "artist_4",
                "master_metadata_album_album_name": "album_5",
                "skipped": True,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "track_1",
                "master_metadata_album_artist_name": "playlist_artist_1",
                "master_metadata_album_album_name": "album_6",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-09-11T23:12:05Z",
                "master_metadata_track_name": "playlist_track_2",
                "master_metadata_album_artist_name": "playlist_artist_2",
                "master_metadata_album_album_name": "album_6",
                "skipped": False,
                "ms_played": 1,
            },
        ]
    )


@pytest.fixture
def mock_mixed_listening_history(mock_listening_history):
    """Create a short mock listening history containing both songs and podcasts"""
    podcast_episodes = pd.DataFrame(
        [
            {
                "ts": "2024-10-30T07:00:00Z",
                "master_metadata_track_name": None,
                "master_metadata_album_artist_name": None,
                "master_metadata_album_album_name": None,
                "episode_name": "podcast_episode_1",
                "episode_show_name": "podcast_1",
                "skipped": False,
                "ms_played": 1,
            },
            {
                "ts": "2024-10-30T07:00:00Z",
                "master_metadata_track_name": None,
                "master_metadata_album_artist_name": None,
                "master_metadata_album_album_name": None,
                "episode_name": "podcast_episode_2",
                "episode_show_name": "podcast_2",
                "skipped": False,
                "ms_played": 1,
            },
        ]
    )
    mock_listening_history["episode_name"] = None
    mock_listening_history["episode_show_name"] = None
    return pd.concat([mock_listening_history, podcast_episodes])


# ██     ██  ██████      ████████ ███████ ███████ ████████ ███████
# ██    ██  ██    ██        ██    ██      ██         ██    ██
# ██   ██   ██    ██        ██    █████   ███████    ██    ███████
# ██  ██    ██    ██        ██    ██           ██    ██         ██
# ██ ██      ██████         ██    ███████ ███████    ██    ███████


def test_read_listening_history_json():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    listening_history = spotify_crapped.read_listening_history_json(path)
    assert len(listening_history) == 23


def test_load_playlist_from_csv():
    path = pathlib.Path(__file__).parent / "data" / "deep_sleep.csv"
    playlist = spotify_crapped.read_playlist_from_csv(path)
    assert len(playlist) == 228


def test_remove_secondary_artists_from_playlist(mock_dirty_playlist):
    playlist = spotify_crapped.remove_secondary_artists_from_playlist(
        spotify_crapped.rename_playlist_fields(mock_dirty_playlist)
    )
    assert playlist.iloc[1]["master_metadata_album_artist_name"] == "playlist_artist_2"


def test_rename_playlist_fields(mock_dirty_playlist):
    playlist = spotify_crapped.rename_playlist_fields(mock_dirty_playlist)
    assert "master_metadata_album_artist_name" in playlist.columns
    assert "master_metadata_track_name" in playlist.columns


# ███████ ██ ██      ████████ ███████ ██████      ████████ ███████ ███████ ████████ ███████
# ██      ██ ██         ██    ██      ██   ██        ██    ██      ██         ██    ██
# █████   ██ ██         ██    █████   ██████         ██    █████   ███████    ██    ███████
# ██      ██ ██         ██    ██      ██   ██        ██    ██           ██    ██         ██
# ██      ██ ███████    ██    ███████ ██   ██        ██    ███████ ███████    ██    ███████


def test_filter_playlist_from_history(mock_clean_playlist, mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)

    playlist_filter = spotify_crapped.filter_playlist_from_history(
        lh.listening_history, mock_clean_playlist
    )
    lh.add_filter(playlist_filter)
    assert len(lh.filtered_history) == len(mock_listening_history) - len(
        mock_clean_playlist
    )


def test_remove_non_songs(mock_mixed_listening_history, mock_listening_history):
    assert len(mock_mixed_listening_history) != len(mock_listening_history)
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_mixed_listening_history)
    assert len(lh.listening_history) == len(mock_listening_history)


def test_filter_by_artists(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    artists_filter = spotify_crapped.filter_by_artists(
        lh.listening_history, ["artist_1", "artist_2"]
    )
    lh.add_filter(artists_filter)
    assert len(lh.filtered_history) == 5
    lh.reset_filters()
    artists_filter_notpresent = spotify_crapped.filter_by_artists(
        lh.listening_history, ["non_artist"]
    )
    lh.add_filter(artists_filter_notpresent)
    assert len(lh.filtered_history) == 0


def test_filter_by_not_skipped(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    not_skipped_filter = spotify_crapped.filter_by_not_skipped(lh.listening_history)
    lh.add_filter(not_skipped_filter)
    assert len(lh.filtered_history) == len(mock_listening_history) - 1


def test_filter_by_years(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    years_filter = spotify_crapped.filter_by_years(lh.listening_history, [2024])
    lh.add_filter(years_filter)
    assert len(lh.filtered_history) == len(mock_listening_history) - 1
    lh.reset_filters()
    years_filter = spotify_crapped.filter_by_years(lh.listening_history, [2021])
    lh.add_filter(years_filter)
    assert len(lh.filtered_history) == 0


# ███████  ██████  ██████  ████████     ████████ ███████ ███████ ████████ ███████
# ██      ██    ██ ██   ██    ██           ██    ██      ██         ██    ██
# ███████ ██    ██ ██████     ██           ██    █████   ███████    ██    ███████
#      ██ ██    ██ ██   ██    ██           ██    ██           ██    ██         ██
# ███████  ██████  ██   ██    ██           ██    ███████ ███████    ██    ███████


def test_get_top_artists_by_playtime(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    top_artists = lh.get_top_artists_by_playtime()
    assert top_artists.iloc[0]["master_metadata_album_artist_name"] == "artist_2"


def test_get_top_songs_by_count(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    top_songs = lh.get_top_songs_by_count()
    assert top_songs.iloc[0]["master_metadata_track_name"] == "track_4"
    assert top_songs.iloc[0]["master_metadata_album_artist_name"] == "artist_3"
    assert top_songs.iloc[0]["play_count"] == 2


def test_get_top_albums(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    top_albums = lh.get_top_albums_by_count()
    assert top_albums.iloc[0]["master_metadata_album_album_name"] == "album_3"
    assert top_albums.iloc[0]["master_metadata_album_artist_name"] == "artist_3"
    assert top_albums.iloc[0]["play_count"] == 3


#  ██████ ██       █████  ███████ ███████     ████████ ███████ ███████ ████████ ███████
# ██      ██      ██   ██ ██      ██             ██    ██      ██         ██    ██
# ██      ██      ███████ ███████ ███████        ██    █████   ███████    ██    ███████
# ██      ██      ██   ██      ██      ██        ██    ██           ██    ██         ██
#  ██████ ███████ ██   ██ ███████ ███████        ██    ███████ ███████    ██    ███████


def test_print_history(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    print(lh)


def test_add_history_from_path():
    path = pathlib.Path(__file__).parent / "data" / "test_data.json"
    lh = spotify_crapped.ListeningHistory()
    lh.add_history_from_path(path)
    assert len(lh.listening_history) == 23
    extra_data_path = pathlib.Path(__file__).parent / "data" / "test_data_2.json"
    lh.add_history_from_path(extra_data_path)
    assert len(lh.listening_history) == 26


def test_add_history(mock_listening_history):
    lh = spotify_crapped.ListeningHistory()
    lh.add_history(mock_listening_history)
    assert len(lh.listening_history) == len(mock_listening_history)
    lh.add_history(mock_listening_history)
    assert len(lh.listening_history) == 2 * len(mock_listening_history)
