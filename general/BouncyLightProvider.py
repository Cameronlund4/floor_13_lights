from LightProvider import LightProvider

class BouncyLightProvider(LightProvider):
    ind = 1
    direct = True

    def __init__(self, provider):
        super(BouncyLightProvider, self).__init__()
        self.provider = provider

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)
        for i in range(len(pixels)):
            if abs(i - self.ind) <= 2:
                if abs(i - self.ind) <= 1:
                    pixels[i] = [0, 0, 0]
                else:
                    pixels[i] = [0, 255, 0]
            else:
                pixels[i] = fakePixels[i]
        
        if (self.ind >= (len(fakePixels)-5)):
            self.direct = False
        elif (self.ind <= 5):
            self.direct = True
        
        print(self.ind)

        if (self.direct):
            self.ind += 1
        else:
            self.ind -= 1