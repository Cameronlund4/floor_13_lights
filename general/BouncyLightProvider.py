from LightProvider import LightProvider

class BouncyLightProvider(LightProvider):
    ind = 0
    direct = True

    def __init__(self, provider):
        super(BouncyLightProvider, self).__init__()
        self.provider = provider

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)
        for i in range(len(pixels)):
            if i == ind:
                pixels[i] == [0, 255, 0]
            else:
                pixels[i] = fakePixels[i]
        
        if (ind >= len(fakePixels)) :
            direct = False
        elif (ind <= 0):
            direct = True
        
        if (direct):
            ind += 1
        else:
            ind -= 1