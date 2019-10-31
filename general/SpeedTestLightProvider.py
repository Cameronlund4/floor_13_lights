from LightProvider import LightProvider

class SpeedTestLightProvider(LightProvider):
    parity = False

    def __init__(self):
        super(SpeedTestLightProvider, self).__init__()

    # Overrides parent
    def providePixels(self, pixels):
        for i in range(len(pixels)):
            pixels[i] = [255, 0, 0] if ((i % 2 == 0) if self.parity else (i % 2 != 0)) else [0, 0, 0]
        self.parity = not(self.parity)