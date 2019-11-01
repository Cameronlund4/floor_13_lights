from LightProvider import LightProvider
import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import time
import threading
import sys
import numpy
import math


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


def light_percentage_cos(time_until, duration):
    return (
        math.cos(
            (2*math.pi*time_until) * pulseMult
            / duration
        ) + 1
    ) / 2


def light_percentage_neg_abs_sin(time_until, duration):
    return (
        -1 * abs(
            math.sin(
                (math.pi*time_until) * pulseMult
                / duration
            )
        ) + 1
    )


def light_percentage_abs_sin(time_until, duration):
    return (
        abs(
            math.sin((
                (math.pi*time_until) * pulseMult
                / duration) + (math.pi/2)
            )
        )
    )


def flash_lights():
    global beatIndex
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
                if not beatIndex:
                    print("Finding beat failed!")
                    time.sleep(2)
                    continue
            # Use beatIndex to sleep until the next beat
            if (beatIndex < len(segments)-1):  # TODO Better handle the last note
                nextBar = segments[beatIndex]
            else:
                nextBar = None
            # If we have a bar, find the light percentage we want
            if nextBar:
                nextBar = nextBar
                # While we're still in this beat and don't have a new song
                loudness = get_loudness(nextBar["start"])
                #print("Loudness:", loudness)
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
                    brightness = percentage
                    # 1 - \
                    #     (
                    #         (1 - percentage) *
                    #         (1-(loudness /
                    #             lightCacheData["track"]["loudness"]))
                    #     )
                beatIndex += 1
                #print("Beat hit!")
        else:
            brightness = 0
            # Make the lights not be doing anything
            beatIndex = None


def pull_spot_data():
    # Start pulling data from spotify
    global beatIndex
    global brightness
    global resetIndex
    global segmentIndex
    global lightSong
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

                timbreSums = []
                for segment in lightSongData["segments"]:
                    timbreSum = 0
                    for timbre in segment["timbre"]:
                        timbreSum += timbre
                    timbreSums.append(timbreSum)
                hist, bin_edges = numpy.histogram(timbreSums, bins="auto")
                print(hist)
                print(bin_edges)
                highest = 0
                for ind, h in enumerate(hist):
                    if h > hist[highest]:
                        print("New high:", ind, h)
                        print(h, ">", hist[highest])
                        highest = ind
                        # No break, we want the rightmost highest
                print("Highest:", highest)
                lowThresh = bin_edges[highest]
                highThresh = bin_edges[highest+1]
                print("Low thresh:", lowThresh, "High thresh:", highThresh)
                for segment in lightSongData["segments"]:
                    timbreSum = 0
                    for timbre in segment["timbre"]:
                        timbreSum += timbre
                    if ((timbreSum >= lowThresh) and (timbreSum < highThresh)):
                        if ((segment["loudness_max"] >= -30)):
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


flashingThread = threading.Thread(target=flash_lights)
flashingThread.setDaemon(True)
flashingThread.start()

pullThread = threading.Thread(target=pull_spot_data)
pullThread.setDaemon(True)
pullThread.start()


class SpotifyBrightnessWrapper(LightProvider):
    provider = None

    def __init__(self, provider):
        super(SpotifyBrightnessWrapper, self).__init__()
        self.provider = provider

    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color

    # Overrides parent
    def providePixels(self, pixels):
        global brightness
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)

        for i in range(len(pixels)):
            pixels[i] = self.gradient(brightness, fakePixels[i], [0, 0, 0])