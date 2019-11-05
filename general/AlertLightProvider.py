from LightProvider import LightProvider
import random


class AlertLightProvider(LightProvider):
    counter = 0
    blink = 16

    def __init__(self, blink=16):
        super(AlertLightProvider, self).__init__()
        self.blink = blink

    # Set next frame of pixels
    def providePixels(self, pixels):
        self.counter += 1
        if self.counter < (self.counter/2):
            for i in range(len(pixels)):
                pixels[i] = [255, 0, 0]
        else:
            for i in range(len(pixels)):
                pixels[i] = [0, 0, 0]

        self.counter %= 8
