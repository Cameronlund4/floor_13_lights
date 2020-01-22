from LightProvider import LightProvider


class RainLightWrapper(LightProvider):
    providerLeft = None
    providerRight = None
    centerPixel = 0

    def __init__(self, providerLeft, providerRight, centerPixel, switchDir=False):
        super(RainLightWrapper, self).__init__()
        self.providerLeft = providerLeft
        self.providerRight = providerRight
        self.centerPixel = centerPixel
        self.switchDir = switchDir

    # Set next frame of pixels
    def providePixels(self, pixels):
        fakePixelsLeft = [None] * (len(pixels)-self.centerPixel) # centerPixel+1 -> len(pixels)
        fakePixelsRight = [None] * (self.centerPixel) # 0 -> centerPixel
        
        self.providerLeft.providePixels(fakePixelsLeft)
        self.providerRight.providePixels(fakePixelsRight)

        for i in range(0, self.centerPixel):
            pixels[i] = (fakePixelsRight[i] if not(self.switchDir) else fakePixelsRight[::-1][i])

        acc = 0
        for i in range(len(pixels)-1, self.centerPixel-1, -1):
            pixels[i] = (fakePixelsLeft[acc] if not(self.switchDir) else fakePixelsLeft[::-1][acc])
            acc += 1
