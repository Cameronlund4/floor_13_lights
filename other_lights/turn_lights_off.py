import board
import neopixel
import time
import threading
import math
import threading
import time
import os


num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D18, num_of_pixels, brightness=0, auto_write=False, pixel_order=neopixel.GRB)


