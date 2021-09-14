from eyed3 import load as eyed3_loader
from eyed3.id3 import ID3_V2_3
from urllib.request import urlopen
from dotenv import load_dotenv
from os import getenv as env
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

spotify_client_id = env('SPOTIFY_CLIENT_ID')
spotify_client_secret = env('SPOTIFY_CLIENT_SECRET')

def hhmmss_to_minutes(t):
    l = list(map(int, t.split(':')))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600))) / 60

def add_audio_meta(track_info, track_path):
    t = track_info
    audio_file = eyed3_loader(track_path)
    if not audio_file.tag:
        audio_file.initTag()
    tag=audio_file.tag
    tag.artist = t['artists'][0]['name']
    tag.album = t['album']['name']
    tag.title = t['name']
    tag.album_artist = t['album']['artists'][0]['name']
    tag.recording_date = t['album']['release_date'][0:4]
    tag.images.set(3, urlopen(t['album']['images'][0]['url']).read() , 'image/jpeg', u'cover')
    tag.save(version=ID3_V2_3)

spotify_instance = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))
