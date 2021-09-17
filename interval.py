from apscheduler.schedulers.background import BlockingScheduler
from app import playlist_deconstruct, playlist_dl
from dotenv import load_dotenv
from os import getenv as env
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

load_dotenv()

spotify_playlist_url = env('SPOTIFY_PLAYLIST_URL')
interval_duration = int(env('RUN_EVERY_MINUTES'))

def run():
    track_list = playlist_deconstruct(spotify_playlist_url)
    playlist_dl(track_list)

def listen_to_exceptions(event):
    if event.exception:
        exception_info = type(event.exception), event.exception, event.exception.__traceback__
        print(exception_info)

sched = BlockingScheduler()
sched.add_listener(listen_to_exceptions, EVENT_JOB_EXECUTED |  EVENT_JOB_ERROR)
sched.add_job(run, 'interval', minutes=interval_duration)

sched.start()
