from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
import sys
from os import getenv as env
from os import remove
from os import path
import requests
from io import BytesIO
from dotenv import load_dotenv
from utils import hhmmss_to_minutes, add_audio_meta

load_dotenv()

folder_path = env('FOLDER_PATH')
youtube_duration_limit = env('YOUTUBE_DURATION_LIMIT')
spotify_playlist_url = env('SPOTIFY_PLAYLIST_URL')
spotify_client_id = env('SPOTIFY_CLIENT_ID')
spotify_client_secret = env('SPOTIFY_CLIENT_SECRET')

download_path = path.join(path.dirname(__file__), folder_path)

sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))

def main(spotify_playlist_url, youtube_duration_limit):
    spotify_playlist = {}
    try:
        spotify_playlist = sp.playlist_tracks(spotify_playlist_url)
        if not spotify_playlist['items']:
            raise Exception('Error! Cannot download from an empty playlist.')
    except Exception as e:
        sys.exit(e)
    track_list = spotify_playlist['items']
    if spotify_playlist['next'] is not None:
        track_list.extend(sp.next(spotify_playlist)['items'])
    referencedict={}
    for i in track_list:
        t = i['track']
        search_query = t['artists'][0]['name'] + ' - ' + t['name'] + ' - ' + t['album']['name'] + ' Audio'
        search_result = {}
        choosen_video = None
        try:
            search_result = VideosSearch(search_query, limit=4).result()['result']
            if not search_result:
                raise Exception('Error! Could not find any results on Youtube.')
        except Exception as e:
            sys.exit(e)
        for item in search_result:
            if hhmmss_to_minutes(item['duration']) < int(youtube_duration_limit):
                choosen_video = item['id']
                break
        audio_buffer = BytesIO()
        try:
            audio = YouTube(f'http://youtu.be/{choosen_video}').streams.get_audio_only()
            audio.stream_to_buffer(audio_buffer)
        except Exception as e:
            sys.exit(f'Error! Could not download the audio stream from Youtube: {e}.')
        file_path = path.join(download_path, t['artists'][0]['name'] + ' - ' + t['name'] + '.mp3')
        try:
            AudioSegment.from_file(BytesIO(audio_buffer.getvalue())).export(file_path, format='mp3', bitrate='128k')
        except Exception as e:
            sys.exit(f'Error! Could not convert the file to mp3: {e}.')
        add_audio_meta(t, file_path)
