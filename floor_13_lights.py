import board
import neopixel
import time
import threading
import math
import threading
import time
import os
import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy


os.environ['SPOTIPY_CLIENT_ID'] = 'fa8917d98c1a4adeb03f809f486468c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd7d0222ee8c744b8ad191bd1e19c9d01'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'

username = 'staticshadow'
scope = "playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private user-read-email user-library-modify user-library-read user-follow-modify user-follow-read user-read-recently-played user-top-read streaming app-remote-control"

flash_time_m = .25

current_time_song = 0
song_time_sys = 0
lightSong = None
lightSongData = None
segments = []

resetIndex = False
beatIndex = 0
segmentIndex = 0

pulseTo = "segments"
pulseMult = 1  # Multiplying by 2 for bars so that it cycles twice per bar, seems to work more with most songs TODO Make this based on something in the song?

sp = spotipy.Spotify()

brightness = 0
num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1.0, auto_write=False, pixel_order=neopixel.RGB)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    # if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
    return (r, g, b)


def brightnessPulse():
    global pixels
    while True:
        for i in range(0, 100, 5):
            perc = i / 100.0
            pixels.brightness = perc
            pixels.show()
            time.sleep(0.01)
        for i in range(100, 0, -5):
            perc = i / 100.0
            pixels.brightness = perc
            pixels.show()
            time.sleep(0.01)


def rainbow():
    global pixels
    j = 0
    while True:
        j += int(brightness * 10)
        j %= 255
        for i in range(num_of_pixels):
            pixel_index = (i * 256 // num_of_pixels) + 2 * j
            #print("\t => Pixel_index = {}".format(pixel_index))
            pixels[i] = wheel(pixel_index & 255)
            #print("Setting pixel {} to {}".format(i, pixel_index & 255))
        #print("Finished iteration for {}".format(j))
        pixels.brightness = brightness
        #print("Brightness => {}".format(brightness))
        pixels.show()


def gradient(color1, color2):
    global pixels

    r1 = color1[0]
    g1 = color1[1]
    b1 = color1[2]

    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]
    for i in range(num_of_pixels):
        p = i / float(num_of_pixels - 1)
        r = int((1.0-p) * r1 + p * r2 + 0.5)
        g = int((1.0-p) * g1 + p * g2 + 0.5)
        b = int((1.0-p) * b1 + p * b2 + 0.5)
        pixels[i] = (r, g, b)
    pixels.show()


def newToken():
    return util.prompt_for_user_token(username, scope)


def time_until(song_seconds):
    delay = (song_seconds - current_time_song) - (time.time() - song_time_sys)
    return delay


def get_loudness(song_seconds):
    global segmentIndex

    if (lightSongData):
        segments = lightSongData["segments"]
        for i in range(segmentIndex, len(segments)):
            if (float(segments[i]["start"]) <= song_seconds):
                if float(segments[i]["start"]+float(segments[i]["duration"])) > song_seconds:
                    segmentIndex = i
                    return segments[i]["loudness_max"]
    else:
        return None


def flash_lights():
    global beatIndex
    global pixels
    global brightness
    global resetIndex
    global segmentIndex

    while True:
        if (resetIndex):
            beatIndex = None
            resetIndex = False
            segmentIndex = 0
            max_loudness = -100
        lightCache = lightSong
        lightCacheData = lightSongData
        if (lightCache):
            song_id = lightCache["item"]["id"]
            # If we don't know where we are in the song, find it
            # TODO Try doing this for every next index
            if not beatIndex:
                # TODO Binary search!
                for ind, bar in enumerate(segments):
                    if time_until(bar["start"]+bar["duration"]) > 0:
                        beatIndex = ind
                        break
            # Use beatIndex to sleep until the next beat
            if (beatIndex < len(segments)):
                nextBar = segments[beatIndex]
            else:
                nextBar = None
            # If we have a bar, find the light percentage we want
            if nextBar:
                nextBar = nextBar
                # While we're still in this beat and don't have a new song
                loudness = get_loudness(nextBar["start"])
                print("Loudness:", loudness)
                while time_until(nextBar["start"]+nextBar["duration"]) > 0 and (not resetIndex):
                    #     if (time_until(nextBar["start"]) > 0):
                    #         brightness = 0;
                    #     else:
                    percentage = light_percentage_abs_sin(time_until(
                        segments[beatIndex + 1]["start"]), segments[beatIndex + 1]["start"] - nextBar["start"])
                    if (loudness > 0):
                        loudness = 0
                    loudness /= 30
                    if (loudness > 0):
                        loudness = 0
                    brightness = 1-percentage
                    # 1 - \
                    #     (
                    #         (1 - percentage) *
                    #         (1-(loudness /
                    #             lightCacheData["track"]["loudness"]))
                    #     )
                beatIndex += 1
        else:
            brightness = 0
            # Make the lights not be doing anything
            beatIndex = None


def light_percentage_cos(time_until, duration):
    return (
        math.cos(
            (2*math.pi*time_until) * pulseMult
            / duration
        ) + 1
    ) / 2


def light_percentage_abs_sin(time_until, duration):
    return (
        -1 * abs(
            math.sin(
                (math.pi*time_until) * pulseMult
                / duration
            )
        ) + 1
    )


flashingThread = threading.Thread(target=flash_lights)
flashingThread.setDaemon(True)
flashingThread.start()

rainbowThread = threading.Thread(target=rainbow)
rainbowThread.setDaemon(True)
rainbowThread.start()

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
        if (not lightSong) or (lightSong["item"]["id"] != currentSong["item"]["id"]):
            print("Now playing", currentSong["item"]["name"])
            lightSong = None
            lightSongData = None
            resetIndex = True
            print("Grabbing analysis data!")
            lightSongData = sp.audio_analysis(song_id)
            print("\t-> Data aquired!")

            for segment in lightSongData["segments"]:
                if ((segment["duration"] >= .30) and (segment["duration"] <= .32)):
                    segments.append(segment)

        # Set the current song for the visuals tasks
        lightSong = currentSong

        # print(currentSong["item"]["name"], "@",
        #       currentSong["progress_ms"] / 1000, "seconds")
    else:
        print("No music currently playing!")
        lightSong = None
        lightSongData = None
    time.sleep(1)
