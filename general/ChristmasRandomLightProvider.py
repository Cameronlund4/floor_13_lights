from LightProvider import LightProvider
import random


class ChristmasRandomLightProvider(LightProvider):
    steps = []
    treeColor = [31, 77, 9]
    christmasColors = [
        [234, 13, 13],
        [251, 111, 36],
        [251, 242, 26],
        [10, 83, 222],
        [137, 52, 184]
    ]

    example_light = ["color", "timeAlive"]
    liveLights = None
    MIN_DISTANCE = 6
    WIDTH = 3 # Should be odd
    START_EDGE_BRIGHTNESS = .75 # Percent of brightness of the total light
    END_EDGE_BRIGHTNESS = .25 # Percent of brightness of the total light
    MAX_LIGHTS = 10
    RENDER_PERCENTAGE = .1
    MIN_FADE_BRIGHTNESS = .25

    def __init__(self, light_width=6, picks=50):
        super(ChristmasRandomLightProvider, self).__init__()

    # choice = random.choice(colors)
    def pick_light_pos(self, MIN_DISTANCE, liveLights, good_indexes=[]):
        if not good_indexes:
            # TODO Find good indexes
            pass
        return 0 # TODO Implement

    def gradient(self, percent, colorA, colorB):
            color = [0, 0, 0]
            for i in range(3):
                color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
            return color

    # Set next frame of pixels
    def providePixels(self, pixels):
        # If we don't have our array, make them with the length of our lights
        if not self.liveLights:
            self.liveLights = [None] * len(pixels)
            self.liveLights[149] = [[234, 13, 13], 10.0]

        # Fill the cache with green (the color of the christmas light)
        cache = [self.treeColor] * len(pixels)

        # TODO Draw tree and lights
        for i in range(len(self.liveLights)):
            if not self.liveLights[i]:
                continue

            light = self.liveLights[i]

            cache[i] = light[0]

            # TODO Finish
            # # Draw the light centered at i
            # for j in range(i-((self.WIDTH-1)/2), 1+i+((self.WIDTH-1)/2)):
            #     # Make the center full brightness, make the edges less bright

            #     percentage = abs(i-j)

        # Draw the cache into the pixels
        for i in range(len(cache)):
            pixels[i] = cache[i]