from LightProvider import LightProvider
import random

class StarLightWrapper(LightProvider):
    provider = None
    branch_low = 0
    branch_high = 10
    minBright = 0
    branch_out_last = 0
    branch_its = 5
    branch_acc = 0
    atBeginning = False
    cloud_color = [255, 255, 255]

    def __init__(self, provider, branch_low, branch_high, *, branch_its=5, minBright=0, atBeginning=False):
        super(StarLightWrapper, self).__init__()
        self.provider = provider
        self.branch_low = branch_low
        self.branch_high = branch_high
        self.minBright = minBright
        self.cloud_color = cloud_color
        self.branch_its = branch_its
        self.branch_out_last = random.randint(branch_low, branch_high)
        self.atBeginning = atBeginning

    def cloud(self, index, color, branch_out):
        if index <= branch_out:
            return self.gradient(((branch_out-index)*.75)/(branch_out), [0,0,0], [255, 255, 0])
        else:
            return color

    def randCloudDirection(self, branch_out):
        if (branch_out == self.branch_high):
            return branch_out - 1
        elif (branch_out == self.branch_low):
            return branch_out + 1
        else:
            return branch_out + random.randint(-1, 1)

    # Set next frame of pixels
    def providePixels(self, pixels):
        fakePixels = [None] * len(pixels)
        self.provider.providePixels(fakePixels)

        if (self.branch_acc % self.branch_its == 0):
            self.branch_out_last = self.randCloudDirection(self.branch_out_last)
            self.branch_acc = 0

        self.branch_acc += 1

        for ind, color in enumerate(fakePixels):
            pixels[ind] = self.cloud(ind if not(self.atBeginning) else len(pixels)-1-ind, color, self.branch_out_last)
