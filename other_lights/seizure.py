import board
import neopixel
import time
import threading
import math
import threading
import time
import os


brightness_num = 255/255
num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D21, num_of_pixels, brightness=brightness_num, auto_write=False, pixel_order=neopixel.GRB)


def seizure():
    global pixels
    pixels.fill((255, 255, 255))
    while True:
        if pixels.brightness == 0:
            pixels.brightness = 1.0
            pixels.show()
        else:
            pixels.brightness = 0.0
            pixels.show()
        time.sleep(0.035)
seizure()
