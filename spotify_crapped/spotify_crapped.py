"""Module for interactig with spotify listening history. Imports a JSON file with listening history
"""

import csv
import json
import re
from typing import Any, Dict, List

import pandas as pd


def read_listening_history_json(path: str) -> pd.DataFrame:
    """Reads a JSON file with listening history data, removes malformed trailing commas,
    and returns a pandas DataFrame
    """
    with open(path, "r", encoding="UTF-8") as file:
        raw_data = file.read()

    cleaned_data = re.sub(r",\s*([\]}])", r"\1", raw_data)

    data = json.loads(cleaned_data)
    return pd.DataFrame(data)


def remove_unused_fields_from_playlist(playlist: pd.DataFrame) -> pd.DataFrame:
    """Removes all fields from the playlist DataFrame except for the track name and artist name"""
    return playlist[["Track Name", "Artist Name(s)"]]


def remove_secondary_artists_from_playlist(playlist: pd.DataFrame) -> pd.DataFrame:
    """Removes any artists listed after the first artist in the playlist DataFrame"""
    filtered_playlist = playlist.copy()
    filtered_playlist["master_metadata_album_artist_name"] = (
        filtered_playlist["master_metadata_album_artist_name"].str.split(",").str[0]
    )
    return filtered_playlist


def rename_playlist_fields(playlist: pd.DataFrame) -> pd.DataFrame:
    """Renames the fields in the playlist DataFrame to match the listening history DataFrame"""
    return playlist.rename(
        columns={
            "Track Name": "master_metadata_track_name",
            "Artist Name(s)": "master_metadata_album_artist_name",
        }
    )


def load_playlist_from_csv(path: str) -> pd.DataFrame:
    """Loads a playlist from a CSV file

    Arguments:
        path: Path to the CSV file

    Returns:
        DataFrame with the playlist data
    """
    with open(path, "r", encoding="UTF-8") as file:
        playlist = pd.read_csv(file)
    cleaned_playlist = remove_unused_fields_from_playlist(playlist)
    cleaned_playlist = rename_playlist_fields(cleaned_playlist)
    cleaned_playlist = remove_secondary_artists_from_playlist(cleaned_playlist)
    return cleaned_playlist


def prettify_fields(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Makes names of the fields in the listening history DataFrame more human-readable"""
    pretty_history = listening_history.copy()
    pretty_history.rename(
        columns={
            "ts": "Timestamp",
            "master_metadata_track_name": "Track",
            "master_metadata_album_artist_name": "Artist",
            "master_metadata_album_album_name": "Album",
            "ms_played": "Playtime (ms)",
            "play_count": "Play Count",
        },
        inplace=True,
    )
    return pretty_history


def remove_unused_fields_from_history(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Removes unused fields from a listening history DataFrame

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame with unused fields removed
    """

    return listening_history.drop(
        columns=[
            "platform",
            "conn_country",
            "ip_addr",
            "spotify_track_uri",
            "spotify_episode_uri",
            "episode_name",
            "episode_show_name",
            "reason_start",
            "reason_end",
            "shuffle",
            "offline",
            "offline_timestamp",
            "incognito_mode",
        ],
        errors="ignore",
    )


def convert_timestamps_to_datetime(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Converts timestamps in a listening history DataFrame to datetime format

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame with timestamps converted to datetime format
    """
    listening_history["ts"] = pd.to_datetime(
        listening_history["ts"], format="%Y-%m-%dT%H:%M:%SZ"
    )
    return listening_history


def remove_non_songs(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Filters only songs from a listening history DataFrame

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame with only songs
    """
    return listening_history.dropna(subset=["master_metadata_track_name"])


def apply_filters(listening_history: pd.DataFrame, filters: list) -> pd.DataFrame:
    """Applies a list of filters to a listening history DataFrame

    Arguments:
        listening_history: DataFrame with listening history data
        filters: List of conditions that filter the listening history

    Returns:
        DataFrame with filters applied
    """
    combined_filter = pd.Series(True, index=listening_history.index)
    for f in filters:
        combined_filter &= f
    filtered_history = listening_history[combined_filter]
    return filtered_history


def filter_playlist_from_history(
    listening_history: pd.DataFrame, playlist: pd.DataFrame
) -> pd.Series:
    """Filters a listening history DataFrame by removing any songs in the playlist from the history

    Arguments:
        listening_history: DataFrame with listening history data
        playlist: DataFrame with the playlist data to be filtered out

    Returns:
        Series with the filter condition
    """
    return (
        listening_history.merge(
            playlist,
            on=["master_metadata_track_name", "master_metadata_album_artist_name"],
            how="left",
            indicator=True,
        )["_merge"]
        == "left_only"
    )


def filter_by_song_title(listening_history: pd.DataFrame, song_title: str) -> pd.Series:
    """Filters a listening history DataFrame by song title

    Arguments:
        listening_history: DataFrame with listening history data
        song_title: Title of the song to filter

    Returns:
        Series with the filter condition
    """
    return listening_history["master_metadata_track_name"].str.contains(
        song_title, case=False
    )


def filter_by_artists(listening_history: pd.DataFrame, artists: List[str]) -> pd.Series:
    """Filters a listening history DataFrame by a list of artists

    Arguments:
        listening_history: DataFrame with listening history data
        artist: Name of the artist to filter

    Returns:
        Series with the filter condition
    """
    return listening_history["master_metadata_album_artist_name"].isin(artists)


def filter_by_not_skipped(listening_history: pd.DataFrame) -> pd.Series:
    """Filters a listening history DataFrame by songs that were not skipped

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        Series with the filter condition
    """
    return listening_history["skipped"] == False


def filter_by_years(listening_history: pd.DataFrame, years: List[int]) -> pd.Series:
    """Filters a listening history DataFrame by years

    Arguments:
        listening_history: DataFrame with listening history data
        years: List of years to filter

    Returns:
        Series with the filter condition
    """
    return listening_history["ts"].dt.year.isin(years)


def sort_songs_by_play_count(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Sorts a listening history DataFrame by song play count

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame sorted by song play count
    """
    song_play_counts = (
        listening_history.groupby(
            ["master_metadata_album_artist_name", "master_metadata_track_name"],
            as_index=False,
        )
        .size()
        .rename(columns={"size": "play_count"})
    )

    # Rank songs by play count
    song_play_counts["rank"] = song_play_counts["play_count"].rank(
        ascending=False, method="min"
    )
    # Sort by rank and reset index for cleaner output
    ranked_songs = song_play_counts.sort_values(
        by=["rank", "master_metadata_track_name"]
    ).reset_index(drop=True)

    # Reorganize columns for clarity
    ranked_songs = ranked_songs[
        [
            "rank",
            "master_metadata_track_name",
            "master_metadata_album_artist_name",
            "play_count",
        ]
    ]

    return ranked_songs


def sort_artists_by_play_count(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Sorts a listening history DataFrame by artist play count

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame sorted by artist play count
    """
    return listening_history["master_metadata_album_artist_name"].value_counts()


def sort_artists_by_playtime(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Sorts a listening history DataFrame by artist playtime

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame sorted by artist playtime
    """
    artist_playtime = (
        listening_history.groupby("master_metadata_album_artist_name", as_index=False)
        .agg({"ms_played": "sum"})
        .rename(columns={"ms_played": "total_playtime_ms"})
        .sort_values(by="total_playtime_ms", ascending=False)
    )
    artist_playtime.reset_index(drop=True, inplace=True)
    artist_playtime.index = artist_playtime.index + 1
    artist_playtime["Total Playtime"] = pd.to_timedelta(
        artist_playtime["total_playtime_ms"], unit="ms"
    )
    artist_playtime.drop(columns="total_playtime_ms", inplace=True)
    return artist_playtime


class ListeningHistory:
    """Object containing listening history data and methods for analysis

    Arguments:
        listening_history_path: Path to a spotify listening history json
    """

    def __init__(self):
        self.listening_history = pd.DataFrame()
        self.filtered_history = pd.DataFrame()
        self.filters = []
        return

    def add_history_from_path(self, new_history_path: str) -> None:
        """Adds a new history to the object from a path to a spotify listening history json

        Arguments:
            new_history_path: Path to a spotify listening history json
        """
        new_history_raw: pd.DataFrame = read_listening_history_json(new_history_path)
        self.add_history(new_history_raw)
        return

    def add_history(self, new_history_dataframe: pd.DataFrame) -> None:
        """Adds a new history to the object from a pandas dataframe, removing unused fields
        and converting timestamps from strings to datetime objects

        Arguments:
            new_history_dataframe: DataFrame with listening history data
        """
        new_history_songs_only = remove_non_songs(new_history_dataframe)
        new_history_cleaned_fields = remove_unused_fields_from_history(
            new_history_songs_only
        )
        new_history_cleaned_stamps = convert_timestamps_to_datetime(
            new_history_cleaned_fields
        )
        self.listening_history = pd.concat(
            [self.listening_history, new_history_cleaned_stamps], ignore_index=True
        )
        self.filtered_history = apply_filters(self.listening_history, self.filters)
        return

    def add_filter(self, filter_condition: pd.Series) -> None:
        """Adds a filter to the object and updatees the filtered history

        Arguments:
            filter_condition: Condition to filter the listening history
        """
        self.filters.append(filter_condition)
        self.filtered_history = apply_filters(self.listening_history, self.filters)
        return

    def reset_filters(self) -> None:
        """Removes all applied filters"""
        self.filters = []
        self.filtered_history = apply_filters(self.listening_history, self.filters)
        return

    def get_top_artists_by_count(self) -> pd.Series:
        """Returns the top ten artists in the listening history

        Arguments:
            rank_count: Number of artists to return

        Returns:
            Series with the top `rank_count` artists
        """
        return sort_artists_by_play_count(self.filtered_history)

    def get_top_artists_by_playtime(self) -> pd.DataFrame:
        """Returns the top artists in the listening history by playtime

        Returns:
            DataFrame with the top artists by playtime
        """
        return sort_artists_by_playtime(self.filtered_history)

    def get_top_songs_by_count(self) -> pd.Series:
        """Returns the songs in the listening history by play count"""
        return sort_songs_by_play_count(self.filtered_history)

    def pretty_history(self) -> pd.DataFrame:
        """Returns a pretty version of the listening history"""
        return prettify_fields(self.filtered_history)
