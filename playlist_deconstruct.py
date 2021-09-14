from utils import spotify_instance

def playlist_deconstruct(spotify_playlist_url):
    spotify_playlist = None
    try:
        spotify_playlist = spotify_instance.playlist_tracks(spotify_playlist_url)
        if not spotify_playlist['items']:
            raise Exception('Error! Cannot download from an empty playlist.')
    except Exception as e:
        sys.exit(e)
    track_list = spotify_playlist['items']
    if spotify_playlist['next'] is not None:
        track_list.extend(spotify_instance.next(spotify_playlist)['items'])
    return track_list
