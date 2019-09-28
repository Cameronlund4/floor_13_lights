import spotipy
sp = spotipy.Spotify();
import spotipy.util as util
import spotipy.oauth2 as oauth2
import os
from pprint import pprint
import keyboard
import datetime
import time
import RPi.GPIO as gpio
import threading
flash_time_m = .25;

os.environ['SPOTIPY_CLIENT_ID'] = 'fa8917d98c1a4adeb03f809f486468c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd7d0222ee8c744b8ad191bd1e19c9d01'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'

username = 'staticshadow'
scope = "playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private user-read-email user-library-modify user-library-read user-follow-modify user-follow-read user-read-recently-played user-top-read streaming app-remote-control"

seconds_between_beat = 0.5;
flash_on_time = 0.5;
flash_off_time = 0.5;

def flash_lights():
    gpio.setmode(gpio.BCM)
    FLASHING_GPIO = 18
    gpio.setup(FLASHING_GPIO, gpio.OUT)
    while True:
        gpio.output(FLASHING_GPIO, True)
        time.sleep(flash_on_time)
        gpio.output(FLASHING_GPIO, False)
        time.sleep(flash_off_time)
    
f = threading.Thread(target=flash_lights)

def newToken():
    return util.prompt_for_user_token(username, scope)

analysis_data = {}

while True:
    token = newToken()
    sp = spotipy.Spotify(auth=token)
    currentSong = sp.current_user_playing_track();
    song_id = currentSong["item"]["id"];
    if not analysis_data.get(song_id, None):
        print("Grabbing analysis data!")
        analysis_data[song_id] = sp.audio_analysis(song_id)
        logFile=open('./{}_spot_dump.json'.format(currentSong["item"]["name"]), 'w')
        pprint(analysis_data[song_id], logFile)
        print("Logged!")
        seconds_between_beat = 1/(analysis_data[song_id]["track"]["tempo"]/60)
        flash_on_time = seconds_between_beat * flash_time_m;
        flash_off_time = seconds_between_beat - flash_on_time;

    print(currentSong["item"]["name"], "@", currentSong["progress_ms"] / 1000, "seconds")
    print("\t", seconds_between_beat, flash_on_time, flash_off_time)
    time.sleep(0.5);
