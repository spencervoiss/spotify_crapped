![spotify_crapped_logo_240x240](https://github.com/user-attachments/assets/5263ed61-6064-4a37-bfb7-33ca398336ce)
# Spotify Crapped

Python library and jupyter notebook for visualizing your Spotify listening history, since Wrapped seems to have totally gone off its rocker.

## Setup

In bash, run the following
```
git clone github.com/spencervoiss/spotify_crapped
cd spotify_crapped
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

## Run

- Save your spotify listening history jsons in `data/listening_history/`
- If you want to exclude any playlists from your listening history (such as background study/sleep music), download them as CSVs using [exportify](https://exportify.app) and place the CSVs in `data/playlists_to_exclude`
- In bash, run `jupyter notebook --no-browser --port=8888`, then open your web browser. You should see a long hexadecimal toekn specified in the terminal. Replace {YOUR_TOKEN} in the URL below with that value.
- Go to `https://localhost:8888/notebooks/spotify_crapped.ipynb?token={YOUR_TOKEN}`
- Run, and have fun!