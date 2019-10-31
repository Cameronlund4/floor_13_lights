from LightProvider import LightProvider


class RainLightProvider(LightProvider):
    providerLeft = None
    providerRight = None
    centerPixel = 0

    def __init__(self, providerLeft, providerRight, centerPixel):
        super(RainLightProvider, self).__init__()
        self.providerLeft = providerLeft
        self.providerRight = providerRight
        self.centerPixel = centerPixel

    # Set next frame of pixels
    def providePixels(self, pixels):
        fakePixelsLeft = [None] * (len(pixels)-self.centerPixel) # centerPixel+1 -> len(pixels)
        fakePixelsRight = [None] * (self.centerPixel) # 0 -> centerPixel
        
        self.providerLeft.providePixels(fakePixelsLeft)
        self.providerRight.providePixels(fakePixelsRight)

        for i in range(0, self.centerPixel+1):
            pixels[i] = fakePixelsRight[i]

        acc = 0
        for i in range(len(pixels)-1, self.centerPixel, -1):
            pixels[i] = fakePixelsLeft[acc]
            acc += 1
