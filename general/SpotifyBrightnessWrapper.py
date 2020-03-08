from LightProvider import LightProvider
import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import time
import threading
import sys
import numpy
import math
import os
import statistics

min_duration = 0.4

os.environ['SPOTIPY_CLIENT_ID'] = 'fa8917d98c1a4adeb03f809f486468c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd7d0222ee8c744b8ad191bd1e19c9d01'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'
username = 'vinlomino'
scope = "playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private user-read-email user-library-modify user-library-read user-follow-modify user-follow-read user-read-recently-played user-top-read streaming app-remote-control"
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
doPartify = True
pings = []
paused = True


def newToken():
    return util.prompt_for_user_token(username, scope)


def time_until(song_seconds):
    # print("Time until:", song_seconds)
    # print(song_seconds-current_time_song, current_time_song)
    # print(time.time(), song_time_sys, time.time() - song_time_sys)
    delay = (song_seconds - current_time_song) - (time.time() - song_time_sys)
    # print(">>>>>>", delay)
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


def light_percentage_linear(time_until, duration):
    half_duration = duration / 2
    print(time_until, duration)
    if time_until/duration > 0.5:
        # Go down
        print("> Down", time_until, time_until-half_duration,
              half_duration, (time_until-half_duration)/half_duration)
        return (time_until-half_duration)/half_duration
    else:
        # Go up
        print("> Up", time_until, time_until,
              half_duration, 1-(time_until/half_duration))
        return 1-(time_until/half_duration)


def light_percentage_binary(time_until, duration):
    return 0 if time_until < (duration/2) else 1


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
    global paused

    while True:
        if (resetIndex):
            beatIndex = None
            resetIndex = False
            segmentIndex = 0
            max_loudness = -100
        lightCache = lightSong
        lightCacheData = lightSongData
        if (lightCache and not(paused)):
            song_id = lightCache["item"]["id"]
            # If we don't know where we are in the song, find it
            # TODO Try doing this for every next index
            if not beatIndex:
                print("No beatIndex, searching for it.")
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
                # While we're still in this beat and don't have a new song
                #print("Loudness:", loudness)
                next_time = time_until(segments[beatIndex + 1]["start"])
                duration = next_time-time_until(nextBar["start"])
                while next_time and duration and (next_time > 0) and (not resetIndex):
                    #     if (time_until(nextBar["start"]) > 0):
                    #         brightness = 0;
                    #     else:
                    if (next_time > duration):
                        # print("Bad next time", next_time, duration)
                        next_time = duration
                    if not doPartify:
                        percentage = light_percentage_binary(next_time, duration)
                    else:
                        percentage = light_percentage_abs_sin( #light_percentage_abs_sin
                            next_time, duration)

                    brightness = percentage
                    next_time = time_until(segments[beatIndex + 1]["start"])
                    time.sleep(0.0025)
                beatIndex += 1
                #print("Beat hit!")
        else:
            brightness = 0
            # Make the lights not be doing anything
            beatIndex = None
            time.sleep(.2)

insertBeats = 2
def partify(segments):
    newSegments = [segments[0]]
    # Go through all the segments and add a fake beat inbetween each
    for i in range(1, len(segments)):
        # Grab segments
        thisSegment = segments[i]
        lastSegment = segments[i-1]

        # Create a new fake segment
        splitDif = (float(thisSegment["start"])-float(lastSegment["start"])) / (insertBeats+1)
        for j in range(insertBeats):
            newSegment = {"start": ((splitDif*(j+1))+newSegments[-1]["start"])}
            newSegment["duration"] = splitDif
            newSegments.append(newSegment)

        # Add our real segment into the segments
        newSegments.append(thisSegment)
    return newSegments

def analyze_data_beat():
    global lightSongData
    global segments

    segments = lightSongData["beats"]

def analyze_data_classic():
    global lightSongData
    global segments

    segments = []
    for section in lightSongData["sections"]:
        # Sum the timbres
        timbreSums = []
        for segment in lightSongData["segments"]:
            # if (segment["duration"] >= min_duration):
            if (segment["start"] >= section["start"]) and ((segment["start"] + segment["duration"]) <= (section["start"] + section["duration"])):
                timbreSum = 0
                for timbre in segment["timbre"]:
                    timbreSum += timbre
                timbreSums.append(timbreSum)

        # Figure out which timbres we want
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

        lastUsedBeat = None
        # Find the new segments we want
        for segment in lightSongData["segments"]:
            timbreSum = 0
            for timbre in segment["timbre"]:
                timbreSum += timbre
            if ((timbreSum >= lowThresh) and (timbreSum < highThresh)):
                if ((segment["loudness_max"] >= -30)):
                    if lastUsedBeat:
                        if ((segment["start"] - lastUsedBeat["start"]) >= min_duration):
                            segments.append(segment)
                            lastUsedBeat = segment
                    else:
                        segments.append(segment)
    if doPartify:
        segments = partify(segments)

def analyze_data_advanced():
    global lightSongData
    global segments

    print("Loudnesses")
    loudest = lightSongData["sections"][0]["loudness"]
    for ind in range(1, len(lightSongData["sections"])):
        loudness = lightSongData["sections"][0]["loudness"]
        if loudness > loudest:
            loudest = loudness
        print(loudness)
    print("Loudest: %f" % loudest)

    print("Running analysis")
    segments = []
    # Iterate every section
    for section in lightSongData["sections"]:

        # Grab information about beats that will be used to section our data
        time_sig = section["time_signature"]
        tempo = section["tempo"]
        seconds_per_beat = 1/(tempo/60)
        seconds_per_beat_half = seconds_per_beat / 2

        print("Loudness: %f" % section["loudness"])
        if (abs(loudest - section["loudness"]) > .20):
            print("Making section normal!")
            # Sum the timbres for each segment in this section
            timbreSums = []
            for segment in lightSongData["segments"]:
                # If the segment is in our section, continue. Otherwise, skip
                if (segment["start"] >= section["start"]) and ((segment["start"] + segment["duration"]) <= (section["start"] + section["duration"])):
                    timbreSum = 0
                    for timbre in segment["timbre"]:
                        timbreSum += timbre
                    timbreSums.append(timbreSum)

            # Figure out which timbres we want
            hist, bin_edges = numpy.histogram(timbreSums, bins="auto")
            highest = 0
            for ind, h in enumerate(hist):
                if h > hist[highest]:
                    highest = ind
                    # No break, we want the rightmost highest
            lowThresh = bin_edges[highest]
            highThresh = bin_edges[highest+1]

            lastUsedBeat = None
            # Find the new segments we want
            for segment in lightSongData["segments"]:
                if (segment["start"] >= section["start"]) and ((segment["start"] + segment["duration"]) <= (section["start"] + section["duration"])):
                    timbreSum = 0
                    for timbre in segment["timbre"]:
                        timbreSum += timbre
                    if ((timbreSum >= lowThresh) and (timbreSum < highThresh)):
                        if ((segment["loudness_max"] >= -30)):
                            if lastUsedBeat:
                                if ((segment["start"] - lastUsedBeat["start"]) >= min_duration):
                                    segments.append(segment)
                                    lastUsedBeat = segment
                            else:
                                segments.append(segment)
        else:
            print("Making section beat!")
            for segment in lightSongData["beats"]:
                if (segment["start"] >= section["start"]) and ((segment["start"] + segment["duration"]) <= (section["start"] + section["duration"])):
                    segments.append(segment)
    if doPartify:
        segments = partify(segments)

def pull_spot_data():
    global current_time_song
    global song_time_sys
    global lightSong
    global lightSongData
    global segments
    global resetIndex
    global beatIndex
    global segmentIndex
    global pulseTo
    global pulseMult
    global pings
    global paused
    while True:
        try:
            print("Checking for a song")
            timeAsked = time.time()
            # Read the current song
            token = newToken()
            sp = spotipy.Spotify(auth=token)
            currentSong = sp.current_user_playing_track()
            if currentSong:
                paused = not(currentSong["is_playing"])
                song_id = currentSong["item"]["id"]

                # Sync up our time with the song
                current_time_song_spotify = currentSong["progress_ms"]/1000

                # pingTemp = pings[:]
                # if len(pingTemp) > 5:
                #     stdev = statistics.pstdev(pingTemp)
                #     mean = statistics.mean(pingTemp)
                #     pingTemp = list(filter(lambda x: (abs(x-mean)<=stdev), pingTemp))
                # avgPing = sum(pingTemp)/len(pingTemp) if len(pingTemp) > 0 else 0

                current_time_song = (time.time()-(currentSong["timestamp"]/1000))# + avgPing
                #currentSong["progress_ms"] / 1000
                pings.append((current_time_song-current_time_song_spotify)) # - avgPing
                
                # print("Avg Ping:",avgPing)
                # print("Ping:",(current_time_song-current_time_song_spotify)) 
                # print("Delta: ",avgPing-(current_time_song-current_time_song_spotify))
                # print("------------------")

                song_time_sys = time.time()

                # If we don't have this song's data, get it
                if (not lightSong) or (lightSong["item"]["id"] != currentSong["item"]["id"]):
                    print("Now playing", currentSong["item"]["name"])
                    pings = []
                    lightSong = None
                    lightSongData = None
                    resetIndex = True
                    print("Grabbing analysis data!")
                    lightSongData = sp.audio_analysis(song_id)
                    print("\t-> Data aquired!")

                    analyze_data_advanced()
                else:
                    print("We've got what we need. Not analyzing.")
                # Set the current song for the visuals tasks
                lightSong = currentSong

                # print(currentSong["item"]["name"], "@",
                #       currentSong["progress_ms"] / 1000, "seconds")
            else:
                print("No music currently playing!")
                lightSong = None
                lightSongData = None
            time.sleep(10)
        except:
            print("Exception grabbing song! Spotify issue?")
            time.sleep(.5)


flashingThread = threading.Thread(target=flash_lights)
flashingThread.setDaemon(True)
flashingThread.start()

pullThread = threading.Thread(target=pull_spot_data)
pullThread.setDaemon(True)
pullThread.start()


class SpotifyBrightnessWrapper(LightProvider):
    provider = None
    max_brightness = 0
    min_brightness = 0

    def __init__(self, provider, *, min_brightness=0.3, max_brightness=1):
        super(SpotifyBrightnessWrapper, self).__init__()
        self.provider = provider
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness

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

        percentage = (
            (1-brightness)
            *
            (1-self.min_brightness-(1-self.max_brightness))
        ) + self.min_brightness

        for i in range(len(pixels)):
            pixels[i] = self.gradient(percentage, [0, 0, 0], fakePixels[i])
