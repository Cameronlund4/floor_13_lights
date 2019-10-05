import board
import neopixel
import time
import threading
import math
import threading
import time
import os


num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D21, num_of_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)


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

rainbow()

