from LightProvider import LightProvider

class FrameSkipWrapper(LightProvider):
    frames_to_skip = 0
    provider = None

    def __init__(self, provider, frames_to_skip=1):
        super(FrameSkipWrapper, self).__init__()
        self.provider = provider
        self.frames_to_skip = frames_to_skip

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)
        for i in range(self.frames_to_skip):
            self.provider.providePixels(fakePixels)
        
        for i in range(len(pixels)):
            pixels[i] = fakePixels[i]