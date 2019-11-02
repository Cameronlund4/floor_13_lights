import board
import neopixel
import time
import threading
import math
import os
import random
from GradientFixedLightProvider import GradientFixedLightProvider
from CloudLightWrapper import CloudLightWrapper
from RainLightWrapper import RainLightWrapper
from RainbowLightProvider import RainbowLightProvider
from SexyTimeLightProvider import SexyTimeLightProvider
from SpeedTestLightProvider import SpeedTestLightProvider
from AlternateLightWrapper import AlternateLightWrapper
from BouncyLightProvider import BouncyLightProvider
from OceanLightProvider import OceanLightProvider
from SpotifyBrightnessWrapper import SpotifyBrightnessWrapper


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

leftProvider = CloudLightWrapper((
    SpotifyBrightnessWrapper(RainbowLightProvider())), 25, 50, atBeginning=True)
rightProvider = CloudLightWrapper((
    SpotifyBrightnessWrapper(RainbowLightProvider())), 25, 50, atBeginning=True)
provider = RainLightWrapper(leftProvider, rightProvider, 150)

while True:
    provider.providePixels(pixels)
    pixels.show()
