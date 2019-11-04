from FixedLightProvider import FixedLightProvider
import random


class ChristmasLightProvider(FixedLightProvider):
    steps = []
    christmasColors = [
        [30, 124, 32],
        [182, 0, 0],
        [0, 55, 251],
        [223, 101, 0],
        [129, 0, 219]
    ]

    def __init__(self, light_width=5, picks=50):
        super(ChristmasLightProvider, self).__init__(
            self.gen_random(self.christmasColors, picks, light_width))

    def gen_random(self, colors, picks, light_width):
        output = []
        for i in range(picks):
            for j in range(light_width):
                output.append(random.choice(colors))
            output.append([255,255,255])
        return output