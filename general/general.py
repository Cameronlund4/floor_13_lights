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
from BrightnessLightWrapper import BrightnessLightWrapper
from SpotifyBrightnessWrapper import SpotifyBrightnessWrapper
from FrameSkipWrapper import FrameSkipWrapper
from ChristmasLightProvider import ChristmasLightProvider
from StarLightWrapper import StarLightWrapper


num_of_pixels = 300
center_pixel = 150
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1, auto_write=False, pixel_order=neopixel.GRB)

leftProvider = StarLightWrapper((
    SpotifyBrightnessWrapper(ChristmasLightProvider())), 10, 25, atBeginning=True)
rightProvider = StarLightWrapper((
    SpotifyBrightnessWrapper(ChristmasLightProvider())), 10, 25, atBeginning=True)
provider = BrightnessLightWrapper(
    RainLightWrapper(leftProvider, rightProvider, 150), .5)

while True:
    provider.providePixels(pixels)
    pixels.show()
