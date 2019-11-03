from LightProvider import LightProvider

class BrightnessLightWrapper(LightProvider):
    brightness = 0
    provider = None

    def __init__(self, provider, brightness):
        super(BrightnessLightWrapper, self).__init__()
        self.provider = provider
        self.brightness = brightness

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
            pixels[i] = self.gradient(self.brightness, [0, 0, 0], fakePixels[i])