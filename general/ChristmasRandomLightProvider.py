from LightProvider import LightProvider
import random
import time


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
    WIDTH = 3 # Should be odd
    START_EDGE_BRIGHTNESS = .9 # Percent of brightness of the total light
    END_EDGE_BRIGHTNESS = .65 # Percent of brightness of the total light
    MAX_LIGHTS = 20
    RENDER_PERCENTAGE = .1
    MIN_FADE_BRIGHTNESS = .25
    TIME_FADE_START = 1
    MIN_TIME = .5
    MAX_TIME = 10

    def __init__(self, light_width=6, picks=50):
        super(ChristmasRandomLightProvider, self).__init__()

    # choice = random.choice(colors)
    def pick_light_pos(self, MIN_DISTANCE, liveLights):
        # Find where we can draw
        # Start with array of true
        good_indexes = [True] * len(liveLights)
        # Make 0->WIDTH+1 and MAX->(MAX-(WIDTH+1)) not available
        for i in range(0,WIDTH+2):
            good_indexes[i] = False
        for i in range(len(liveLights)-1, len(liveLights)-3, -1):
            good_indexes[i] = False
        # Make false for anywhere we have lights
        for i, light in enumerate(liveLights):
            if liveLights[i]:
                # prevent out of bounding
                low = 0-self.MIN_DISTANCE
                low = low if (low+i) >= 0 else (-1*i)
                high = 1+self.MIN_DISTANCE
                high = high if (high+i) < len(liveLights) else (len(liveLights)-i)
                # Black out those regions
                for j in range(low, high):
                    good_indexes[i+j] = False

        # Pick an index based on the good indexes we have
        return random.choice([x[0] for x in enumerate(good_indexes) if x[1]])

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

        # Clean up any dead lights, and store time left in those still living
        for i in range(len(self.liveLights)):
            light = self.liveLights[i]

            # Skip nonexistant lights
            if not light:
                continue

            # Figure out how much life the light has left and save it to the light
            light[3] = (light[2]+light[1]) - time.time()
            if light[3] < 0:
                print("Killing light!")
                self.liveLights[i] = None

        # TODO Create any new lights, if we want
        # If we have less lights than we can, decide if we want a new one, and if so, make it
        countLiveLights = len(list(filter(lambda x: x, self.liveLights)))
        if (countLiveLights < self.MAX_LIGHTS):
            # Potentially make as many lights as we can
            for i in range(self.MAX_LIGHTS-countLiveLights):
                print("Creating new light!")
                # TODO Randomly decide if we want a new light now
                index = self.pick_light_pos(self.MIN_DISTANCE, self.liveLights)
                lifetime = self.MIN_TIME + (random.random() * (self.MAX_TIME-self.MIN_TIME))
                light = [random.choice(self.christmasColors), lifetime, time.time(), lifetime]
                self.liveLights[index] = light

        # Fill the cache with green (the color of the christmas light)
        cache = [self.treeColor] * len(pixels)

        # Draw the lights onto the tree
        for i in range(len(self.liveLights)):
            # Only need to draw if a light exists here
            if not self.liveLights[i]:
                continue

            # Prepare the light
            light = self.liveLights[i]
            currentBrightness = 1
        
            # If we want to fade, fade based upon time left
            time_left = light[3] # (light[2]+light[1]) - time.time()
            if (time_left < 0):
                continue
            if time_left < self.TIME_FADE_START:
                currentBrightness = time_left / self.TIME_FADE_START

            # Draw the light centered at i
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

        print("Lights left:",len(list(filter(lambda x: x, self.liveLights))))
        # Draw the cache into the pixels
        for i in range(len(cache)):
            pixels[i] = cache[i]