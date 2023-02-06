# Spotdl

## It's been a year since I created this project and left it unmaintained. But I'll consider getting back into it when I feel like it.

# How it works
This script is used to download songs from a Spotify playlist and convert them to `mp3` format. It uses the Spotify API and the Spotipy library to access the Spotify playlist, the `youtubesearchpython` library to search for the song on YouTube, the `pytube` library to download the song from YouTube, the `pydub` library to convert the downloaded song to `mp3` format, and the `eyed` library to add metadata to the `mp3` file. The script uses a `.env` file to store the Spotify client ID, client secret, and the Spotify playlist URL. It also uses the `TinyDB` library to store the tracklist in a json file, and the `slugify` library to create filenames for the downloaded songs. The script also uses the `loggin` library to log any errors that occur during the process. 

Overall the script performs the following actions:
- Authenticating to Spotify and retrieving the playlist tracks
- Finding the songs on YouTube with the help of a tiny algorithm i have implemented, then downloading them and converting them to mp3
- Adding metadata to the mp3 files
- Updating the local playlist database and removing any removed songs from the playlist.

**NOTICE**: Be aware that this project was created for learning and educational purposes only. I firmly oppose any form of piracy.
