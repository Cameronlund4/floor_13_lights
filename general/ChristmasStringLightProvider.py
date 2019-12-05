from FixedLightProvider import FixedLightProvider
import random


class ChristmasStringLightProvider(FixedLightProvider):
    steps = []
    christmasColors = [
        [234, 13, 13],
        [251, 111, 36],
        [251, 242, 26],
        [10, 83, 222],
        [137, 52, 184]
    ]

    def __init__(self, light_width=6, picks=50):
        super(ChristmasStringLightProvider, self).__init__(
            self.gen_random(self.christmasColors, picks, light_width))

    def gen_random(self, colors, picks, light_width):
        output = []
        for i in range(picks):
            choice = random.choice(colors)
            for j in range(light_width):
                output.append([31, 77, 9])
            for j in range(2):
                output.append(choice)
        return output