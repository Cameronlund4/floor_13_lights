from LightProvider import LightProvider


class BouncyLightProvider(LightProvider):
    ind = 1
    direct = True
    ball_width = 3  # Needs to be odd
    ball_fill = [0, 0, 0]
    ball_border = [255, 255, 255]

    def __init__(self, provider, ball_width=1, ball_fill=[0,0,0], ball_border=[0, 255, 0]):
        super(BouncyLightProvider, self).__init__()
        self.provider = provider
        self.ball_width = (ball_width * 2) + 1
        self.ball_fill = ball_fill
        self.ball_border = ball_border

    # Overrides parent
    def providePixels(self, pixels):
        halfBall = (self.ball_width-1)/2

        # Get fake pixels
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)

        # Render the ball
        for i in range(len(pixels)):
            if abs(i - self.ind) <= halfBall:
                if (abs(i-self.ind) == halfBall):
                    pixels[i] = self.ball_border
                else:
                    pixels[i] = self.ball_fill
            else:
                pixels[i] = fakePixels[i]

        # Handle switching the direction of the ball if necessary
        if (self.ind >= (len(fakePixels)-halfBall)):
            self.direct = False
        elif (self.ind <= halfBall):
            self.direct = True

        # Move the ball
        if (self.direct):
            self.ind += 1
        else:
            self.ind -= 1
