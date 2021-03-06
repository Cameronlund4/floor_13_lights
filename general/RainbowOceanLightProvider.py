from LightProvider import LightProvider
import random


class RainbowOceanLightProvider(LightProvider):
    steps = []
    step = 0
    color = 0
    startInd = 0

    def __init__(self, offset=False, instances=2500, width=5):
        super(LightProvider, self).__init__()
        save = 0
        for i in range(instances//width):
            save += (random.randint(-3, 3)) * 7
            if save > 30:
                save = 30
            elif save < -30:
                save = -30
            self.steps.extend([save] * width)
        self.steps.extend(self.steps[::-1])
        if offset:
            self.color = 255//2

    def wheelify(self, value):
        if value < 0:
            value = 255 + value
        return value % 255

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

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        super().providePixels(fakePixels)
        self.step += 1
        self.step %= len(self.rainbow)
        
        for i in range(len(pixels)):
            pixels[i] = self.gradient(.5, self.rainbow[self.step], fakePixels[i])


    def wrap(self, index, length):
        if index >= len(length):
            return 0
        return index

    # Overrides parent
    def providePixels(self, pixels):
        self.color %= 255
        self.startInd = self.wrap(self.startInd, self.steps)
        nextInd = self.startInd
        for i in range(len(pixels)):
            pixels[i] = self.wheel(self.wheelify(self.color + self.steps[nextInd]))
            nextInd = self.wrap(nextInd+1, self.steps)
        self.startInd += 1
        self.color += 3