from LightProvider import LightProvider

class FixedLightProvider(LightProvider):
    steps = []
    startInd = 0

    def __init__(self, steps):
        super(FixedLightProvider, self).__init__()
        self.steps = steps
    
    def wrap(self, index, length):
        if index >= len(length):
            return 0
        return index

    # Overrides parent
    def providePixels(self, pixels):
        self.startInd = self.wrap(self.startInd, self.steps)
        nextInd = self.startInd
        for i in range(len(pixels)):
            pixels[i] = self.steps[nextInd]
            nextInd = self.wrap(nextInd+1, self.steps)
        self.startInd += 1

