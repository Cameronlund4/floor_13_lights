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
            if i == self.ind:
                print("Draw")
                pixels[i] == [0, 255, 0]
            else:
                pixels[i] = fakePixels[i]
        
        if (self.ind >= len(fakePixels)) :
            self.direct = False
        elif (self.ind <= 0):
            self.direct = True
        
        print(self.ind)

        if (self.direct):
            self.ind += 1
        else:
            self.ind -= 1