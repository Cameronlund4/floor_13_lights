from GradientFixedLightProvider import GradientFixedLightProvider


class RainbowLightProvider(GradientFixedLightProvider):
    def __init__(self, colorIts=3, steps=-5):
        super(FixedLightProvider, self).__init__(
            self.gen_rainbow(steps), colorIts)

    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)

    def gen_rainbow(self, steps):
        colors = []
        for i in range(255, 0, steps):
            colors.append(self.wheel(i))
        return colors
