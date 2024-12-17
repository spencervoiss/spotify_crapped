"""Module for interactig with spotify listening history. Imports a JSON file with listening history
"""

import json
import re

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
            "reason_start",
            "reason_end" "shuffle",
            "offline",
            "offline_timestamp",
            "incognito_mode",
        ]
    )


class ListeningHistory:
    """Object containing listening history data and methods for analysis

    Arguments:
        listening_history_path: Path to a spotify listening history json
    """

    def __init__(self):
        self.listening_history = pd.DataFrame()
        return

    def add_history(self, new_history_path: str) -> None:
        """Adds a new history to the object

        Arguments:
            new_history_path: Path to a spotify listening history json
        """
        new_history = read_history_json(new_history_path)
        self.listening_history = pd.concat(
            [self.listening_history, new_history], ignore_index=True
        )
        return
