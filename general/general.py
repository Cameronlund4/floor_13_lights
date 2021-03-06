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
from ChristmasStringLightProvider import ChristmasStringLightProvider
from StarLightWrapper import StarLightWrapper
from AlertLightProvider import AlertLightProvider
from ChristmasRandomLightProvider import ChristmasRandomLightProvider
from RainbowOceanLightProvider import RainbowOceanLightProvider
from DynamicRainLightWrapper import DynamicRainLightWrapper

num_of_pixels = 300
center_pixel = 150
brightness = 1

pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1, auto_write=False, pixel_order=neopixel.GRB)

leftProvider = RainbowLightProvider(colorIts=7)
rightProvider = RainbowLightProvider(colorIts=7)
provider = SpotifyBrightnessWrapper(
    BrightnessLightWrapper(
        FrameSkipWrapper(
            RainLightWrapper(
                leftProvider,
                rightProvider,
                center_pixel
            ),
            frames_to_skip=3
        ),
        brightness
    ),
    min_brightness=0.1,
    max_brightness=1
)

# leftProvider = RainbowOceanLightProvider() #RainbowLightProvider(colorIts=3)
# rightProvider = RainbowOceanLightProvider() #RainbowLightProvider(colorIts=3)
# provider = SpotifyBrightnessWrapper(
#     BrightnessLightWrapper(
#         RainLightWrapper(
#             leftProvider,
#             rightProvider,
#             center_pixel
#         ),
#         brightness
#     ),
#     min_brightness=0.1,
#     max_brightness=.75
# )

while True:
    provider.providePixels(pixels)
    pixels.show()
