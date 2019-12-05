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

    example_light = ["color", "timeAlive", "timeMade"]
    liveLights = None
    MIN_DISTANCE = 6
    WIDTH = 5 # Should be odd
    START_EDGE_BRIGHTNESS = .75 # Percent of brightness of the total light
    END_EDGE_BRIGHTNESS = .25 # Percent of brightness of the total light
    MAX_LIGHTS = 10
    RENDER_PERCENTAGE = .1
    MIN_FADE_BRIGHTNESS = .25
    TIME_FADE_START = .2
    MIN_TIME = .5
    MAX_TIME = .10

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
            self.liveLights[160] = [[234, 13, 13], 10.0]

        # TODO Clean up dead lights

        # TODO Create any new lights, if we want

        # Fill the cache with green (the color of the christmas light)
        cache = [self.treeColor] * len(pixels)

        # Draw the lights onto the tree
        for i in range(len(self.liveLights)):
            # Only need to draw if a light exists here
            if not self.liveLights[i]:
                continue

            # Grab the light here
            light = self.liveLights[i]

            # TODO Finish
            # Draw the light centered at i
            currentBrightness = 0.5 # TODO Determine based upon time
            for j in range(0-((self.WIDTH-1)//2), 1+((self.WIDTH-1)//2)):
                # Make the center full brightness, make the edges less bright
                # If at center...
                if j == 0:
                    # Make full brightness
                    cache[i+j] = self.gradient(currentBrightness, cache[i+j], light[0])
                    pass
                # If at edge...
                else:
                    # Change light percentage based upon dist from the center pixel
                    # Find percentage for dist. 1 farthest light, 0 closest light, others in between
                    distPercentage = abs(j)/((self.WIDTH-1)/2) 
                    # Convert the dist percentage into a brightness based upon our start and end constraints
                    lightPercentage = self.END_EDGE_BRIGHTNESS + ((self.START_EDGE_BRIGHTNESS-self.END_EDGE_BRIGHTNESS)*(1-distPercentage))
                    # Now figure out this percentage based on the center lights percentage
                    lightPercentage *= currentBrightness

                    # Change the light
                    cache[i+j] = self.gradient(lightPercentage, cache[i+j], light[0])
                    pass

        # Draw the cache into the pixels
        for i in range(len(cache)):
            pixels[i] = cache[i]