import argparse

import spotify_crapped.spotify_crapped as sc
from spotify_crapped.spotify_crapped import ListeningHistory


def main():
    parser = argparse.ArgumentParser(description="Spotify listening history analysis")
    parser.add_argument(
        "listening_history_jsons",
        type=str,
        help="One or more spotify listening history json files",
        nargs="+",
    )
    args = parser.parse_args()
    lh = ListeningHistory()
    for path in args.listening_history_jsons:
        lh.add_history(path)
    lh.add_filter(sc.filter_by_not_skipped(lh.listening_history))
    pretty_fields = sc.prettify_fields(lh.filtered_history)
    deep_sleep = sc.read_playlist_from_csv(
        "/home/rzyxl1/git/spotify_crapped/tests/data/deep_sleep.csv"
    )
    print(deep_sleep)


if __name__ == "__main__":
    main()
