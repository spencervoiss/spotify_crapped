import argparse
from spotify_crapped.spotify_crapped import ListeningHistory

def main():
    parser = argparse.ArgumentParser(description="Spotify listening history analysis")
    parser.add_argument("listening_history_jsons", type=str, help="One or more spotify listening history json files", nargs="+")
    args = parser.parse_args()
    lh = ListeningHistory()
    for path in args.listening_history_jsons:
        lh.add_history(path)
    print(lh.listening_history)

if __name__ == "__main__":
    main()