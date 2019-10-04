import board
import neopixel
import time
import threading
import math
import threading
import time
import os


num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D18, num_of_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)


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
    return (r, g, b) # if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


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
    while True:
        for j in range(255):
            for i in range(num_of_pixels):
                pixel_index = (i * 256 // num_of_pixels) + 2 * j
                #print("\t => Pixel_index = {}".format(pixel_index))
                pixels[i] = wheel(pixel_index & 255)
                #print("Setting pixel {} to {}".format(i, pixel_index & 255))
            #print("Finished iteration for {}".format(j))
            pixels.show()


def light_percentage_cos(time_until, duration):
    return (
        math.cos(
            (2*math.pi*time_until) * pulseMult
            / duration
        ) + 1
    ) / 2


def light_percentage_abs_sin(time_until, duration):
    return (
        abs(
            math.sin(
                (math.pi*time_until) * pulseMult
                / duration
            )
        )
    )


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
        pixels[i] = (r,g,b)
    pixels.show()

def testingBrightness():
    global pixels
    while True:
        for i in range(2, 52):
            j = 1 / i
            temp = abs(math.sin(math.pi * j))
            print("j = {} ------------- temp = {}".format(j, temp))
            pixels.brightness = temp
            pixels.show()
            #time.sleep(0.001)
        for i in range(52, 2, -1):
            j = 1 / i
            temp = abs(math.sin(math.pi * j))
            print("j = {} ------------- temp = {}".format(j, temp))
            pixels.brightness = temp
            pixels.show()
            #time.sleep(0.001)

def seizure():
    global pixels
    while True:
        if pixels.brightness == 0:
            pixels.brightness = 1.0
        else:
            pixels.brightness = 0.0
        time.sleep(0.001)


#gradient((255, 255, 0), (0, 255, 0))

f = threading.Thread(target=seizure)
f.setDaemon(True)
f.start()


rainbow()

