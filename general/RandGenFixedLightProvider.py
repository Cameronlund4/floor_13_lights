from GradientFixedLightProvider import GradientFixedLightProvider
import random

class RandGenFixedLightProvider(GradientFixedLightProvider):
    def __init__(self, colors, colorIts=15, picks=50):
        super(RandGenFixedLightProvider, self).__init__((self.gen_random(colors, picks)), colorIts)

    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color

    def gen_random(self, colors, picks):
        output = []
        for i in range(picks):
            output.append(random.choice(colors))
        return output
