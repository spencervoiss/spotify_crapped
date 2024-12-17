"""Module for interactig with spotify listening history. Imports a JSON file with listening history
"""

import json
import re
from typing import List

import pandas as pd


def read_history_json(path: str) -> pd.DataFrame:
    """Reads a JSON file with listening history data, removes malformed trailing commas,
    and returns a pandas DataFrame
    """
    with open(path, "r", encoding="UTF-8") as file:
        raw_data = file.read()

    cleaned_data = re.sub(r",\s*([\]}])", r"\1", raw_data)

    data = json.loads(cleaned_data)
    return pd.DataFrame(data)


def remove_unused_fields(listening_history: pd.DataFrame) -> pd.DataFrame:
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
        ]
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


def filter_songs_only(listening_history: pd.DataFrame) -> pd.DataFrame:
    """Filters only songs from a listening history DataFrame

    Arguments:
        listening_history: DataFrame with listening history data

    Returns:
        DataFrame with only songs
    """
    return listening_history.dropna(subset=["master_metadata_track_name"])


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


def get_top_n_artists(listening_history: pd.DataFrame, rank_count: int) -> pd.Series:
    """Returns the top ten artists in a listening history DataFrame

    Arguments:
        listening_history: DataFrame with listening history data
        rank_count: Number of artists to return

    Returns:
        Series with the top `rank_count` artists
    """
    return (
        listening_history["master_metadata_album_artist_name"]
        .value_counts()
        .head(rank_count)
    )


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

    def add_history(self, new_history_path: str) -> None:
        """Adds a new history to the object

        Arguments:
            new_history_path: Path to a spotify listening history json
        """
        new_history_raw = read_history_json(new_history_path)
        new_history_songs_only = filter_songs_only(new_history_raw)
        new_history_cleaned_fields = remove_unused_fields(new_history_songs_only)
        new_history_cleaned_stamps = convert_timestamps_to_datetime(
            new_history_cleaned_fields
        )
        self.listening_history = pd.concat(
            [self.listening_history, new_history_cleaned_stamps], ignore_index=True
        )
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

    def get_top_n_artists(self, rank_count: int) -> pd.Series:
        """Returns the top ten artists in the listening history

        Arguments:
            rank_count: Number of artists to return

        Returns:
            Series with the top `rank_count` artists
        """
        return get_top_n_artists(self.filtered_history, rank_count)
