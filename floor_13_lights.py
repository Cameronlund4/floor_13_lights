import math
import threading
import time
import datetime
from pprint import pprint
import os
import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
sp = spotipy.Spotify()
import RPi.GPIO as gpio

os.environ['SPOTIPY_CLIENT_ID'] = 'fa8917d98c1a4adeb03f809f486468c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd7d0222ee8c744b8ad191bd1e19c9d01'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'

username = 'staticshadow'
scope = "playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private user-read-email user-library-modify user-library-read user-follow-modify user-follow-read user-read-recently-played user-top-read streaming app-remote-control"

flash_time_m = .25
FLASHING_GPIO = 21
PWM_GPIO = 12 # pin 12?
current_time_song = 0
song_time_sys = 0
lightSong = None
lightSongData = None

beatIndex = 0
pulseTo = "beats"
pulseMult = 1 # Multiplying by 2 for bars so that it cycles twice per bar, seems to work more with most songs TODO Make this based on something in the song?

# Set up PWM
gpio.setmode(gpio.BOARD)
gpio.setup(PWM_GPIO, gpio.OUT)
gpio.setup(FLASHING_GPIO, gpio.OUT)
p = gpio.PWM(PWM_GPIO, 0.5)
p.start(50)

def flash_lights():
    global beatIndex

    while True:
        if (lightSong):
            song_id = lightSong["item"]["id"]
            if not beatIndex:
                print("Finding the first bar index!")
                for ind, bar in enumerate(lightSongData[pulseTo]):
                    print(bar, "-", ind)
                    if time_until(bar["start"]+bar["duration"]) > 0:
                        beatIndex = ind
                        break
                print("Found beat index:", beatIndex,
                      "/", len(lightSongData[pulseTo]))
                # Find where we should be in the song
            # Use beatIndex to sleep until the next beat
            if (beatIndex < len(lightSongData[pulseTo])):
                nextBar = lightSongData[pulseTo][beatIndex]
            else:
                nextBar = None
            # If we have a bar, find the light percentage we want
            if nextBar:
                print("Running bar!", beatIndex)
                gpio.output(FLASHING_GPIO, True)
                while time_until(nextBar["start"]+nextBar["duration"]) > 0:
                    percentage = light_percentage(time_until(
                        nextBar["start"]+nextBar["duration"]), nextBar["duration"])
                    percentageInt = int(percentage*100)
                    # print("="*percentageInt)
                    p.ChangeFrequency(10+(10*percentage))
                beatIndex += 1
                print("Done bar!")
            else:
                gpio.output(FLASHING_GPIO, False)
                print("No more bars!")
        else:
            # Make the lights not be doing anything crazy TODO Stop pwm?
            beatIndex = None


def light_percentage(time_until, duration):
    return (
        math.cos(
            (2*math.pi*time_until) * pulseMult
            / duration
        ) + 1
    ) / 2


def newToken():
    return util.prompt_for_user_token(username, scope)


def time_until(song_seconds):
    return (song_seconds - current_time_song) - (time.time() - song_time_sys)


# Start our light updating task
f = threading.Thread(target=flash_lights)
f.setDaemon(True)
f.start()

# Start pulling data from spotify
while True:
    # Read the current song
    token = newToken()
    sp = spotipy.Spotify(auth=token)
    currentSong = sp.current_user_playing_track()
    if currentSong:
        song_id = currentSong["item"]["id"]

        # Sync up our time with the song
        current_time_song = currentSong["progress_ms"] / 1000
        song_time_sys = time.time()

        # If we don't have this song's data, get it
        if (not lightSong) or not (lightSong["item"]["id"] == currentSong["item"]["id"]):
            print("Now playing", currentSong["item"]["name"])
            lightSong = None
            lightSongData = None
            print("Grabbing analysis data!")
            lightSongData = sp.audio_analysis(song_id)
            print("\t-> Data aquired!")

        # Set the current song for the visuals tasks
        lightSong = currentSong

        # print(currentSong["item"]["name"], "@",
        #       currentSong["progress_ms"] / 1000, "seconds")
    else:
        print("No music currently playing!")
        lightSong = None
        lightSongData = None
    time.sleep(0.5)
