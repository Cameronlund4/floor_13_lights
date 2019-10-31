import board
import neopixel
import time
import threading
import math
import os
import random
from GradientFixedLightProvider import GradientFixedLightProvider


num_of_pixels = 300
center_pixel = 150
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1, auto_write=False, pixel_order=neopixel.GRB)

blueColors = [
    [59, 171, 253],
    [109, 193, 255],
    [178, 221, 255],
    [6, 205, 244],
    [34, 75, 139],
    [255, 255, 255]
]

provider = GradientFixedLightProvider(blueColors, 10)

while True:
    provider.providePixels(pixels)
    pixels.show()