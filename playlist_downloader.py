from spotipy import Spotify
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
from utils import spotify_instance

load_dotenv()

folder_path = env('FOLDER_PATH')

download_path = path.join(path.dirname(__file__), folder_path)

def playlist_dl(track_list, youtube_duration_limit):
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
            file_path = path.join(download_path, t['artists'][0]['name'] + ' - ' + t['name'] + '.mp3')
        except Exception as e:
            sys.exit(f'Error! Could not download/save the audio stream from Youtube: {e}.')
        try:
            AudioSegment.from_file(BytesIO(audio_buffer.getvalue())).export(file_path, format='mp3', bitrate='128k')
        except Exception as e:
            sys.exit(f'Error! Could not convert the file to mp3: {e}.')
        add_audio_meta(t, file_path)
