import board
import neopixel
import time
import threading
import math
import threading
import time
import os

fraction = 255/255
num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D21, num_of_pixels, brightness=fraction, auto_write=False, pixel_order=neopixel.GRB)

for i in range(num_of_pixels):
    pixels[i] = (255, 255, 255)

pixels.show()
