from apscheduler.schedulers.background import BlockingScheduler
from playlist_downloader import playlist_dl
from playlist_deconstruct import playlist_deconstruct
from dotenv import load_dotenv
from os import getenv as env
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

load_dotenv()

youtube_duration_limit = env('YOUTUBE_DURATION_LIMIT')
spotify_playlist_url = env('SPOTIFY_PLAYLIST_URL')

def run():
    track_list = playlist_deconstruct(spotify_playlist_url)
    playlist_dl(track_list, youtube_duration_limit)

def listen_to_exceptions(event):
    if event.exception:
        exception_info = type(event.exception), event.exception, event.exception.__traceback__
        print(exception_info)

sched = BlockingScheduler()
sched.add_listener(listen_to_exceptions, EVENT_JOB_EXECUTED |  EVENT_JOB_ERROR)
sched.add_job(run, 'interval', seconds=15)

sched.start()

run()
