from RandGenFixedLightProvider import RandGenFixedLightProvider
import random


class RainbowOceanLightProvider(RandGenFixedLightProvider):
    rainbow = []
    step = 0

    def wheel(self, pos):
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
        return (r, g, b)

    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color

            # [255,185,191],
            # [255,212,166],
            # [255,244,184],
            # [222,255,186],
            # [201,209,255],
            # [100,100,100],
            # [150,150,150],
            # [255//2,185//2,191//2],
            # [255//2,212//2,166//2],
            # [255//2,244//2,184//2],
            # [222//2,255//2,186//2],
            # [201//2,209//2,255//2],

    def __init__(self, colorIts=15, picks=50):
        super(RainbowOceanLightProvider, self).__init__([
            [50, 50, 50],
            [150, 150, 150],
            [100, 100, 100],
            [250, 250, 250],
        ], colorIts, picks)

        colors = []
        for i in range(255, 0, -5):
            colors.append(self.wheel(i))

        steps = []
        colors.append(colors[0])
        colors.append(colors[0])
        for i in range(len(colors)-1):
            for j in range(colorIts):
                perc = j/colorIts if i != 0 else 0
                steps.append(self.gradient(perc, colors[i], colors[i+1]))

        self.rainbow = steps


    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        super().providePixels(fakePixels)
        self.step += 1
        self.step %= len(self.rainbow)
        
        for i in range(len(pixels)):
            pixels[i] = self.gradient(.5, self.rainbow[self.step], fakePixels[i])