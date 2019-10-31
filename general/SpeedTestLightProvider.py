from LightProvider import LightProvider

class SpeedTestLightProvider(LightProvider):
    parity = False
    green = 0

    def __init__(self):
        super(SpeedTestLightProvider, self).__init__()

    # Overrides parent
    def providePixels(self, pixels):
        for i in range(len(pixels)):
            if (i == self.green):
                pixels[i] = [0, 255, 0]
            else:
                pixels[i] = [255, 0, 0] if ((i % 2 == 0) if self.parity else (i % 2 != 0)) else [0, 0, 0]
        self.parity = not(self.parity)
        self.green += 1
        if (self.green >= len(pixels)):
            self.green = 0