from LightProvider import LightProvider


class BouncyLightProvider(LightProvider):
    ind = 1
    direct = True

    def __init__(self, provider):
        super(BouncyLightProvider, self).__init__()
        self.provider = provider

    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color

    # Overrides parent
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)
        for i in range(len(pixels)):
            if abs(i - self.ind) <= 30:
                pixels[i] = self.gradient(
                    1-((abs(i - self.ind)/30)*.75), fakePixels[i], [0, 0, 0])
            else:
                pixels[i] = fakePixels[i]

        if (self.ind >= (len(fakePixels)-30)):
            self.direct = False
        elif (self.ind <= 30):
            self.direct = True

        if (self.direct):
            self.ind += 1
        else:
            self.ind -= 1
