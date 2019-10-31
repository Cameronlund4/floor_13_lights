from LightProvider import LightProvider

class AlternateLightWrapper(LightProvider):
    parity = False
    provider = None

    def __init__(self, provider):
        super(AlternateLightWrapper, self).__init__()
        self.provider = provider

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)
        for i in range(len(pixels)):
            pixels[i] = fakePixels[i] if ((i % 2 == 0) if self.parity else (i % 2 != 0)) else [0, 0, 0]
        self.parity = not(self.parity)