from FixedLightProvider import FixedLightProvider
import random


class ChristmasLightProvider(FixedLightProvider):
    steps = []
    christmasColors = [
        [234, 13, 13],
        [251, 111, 36],
        [251, 242, 26],
        [36, 208, 36],
        [10, 83, 222],
        [137, 52, 184]
    ]

    def __init__(self, light_width=5, picks=50):
        super(ChristmasLightProvider, self).__init__(
            self.gen_random(self.christmasColors, picks, light_width))

    def gen_random(self, colors, picks, light_width):
        output = []
        for i in range(picks):
            choice = random.choice(colors)
            for j in range(light_width):
                output.append([0,255,0])
            output.append(choice)
        return output