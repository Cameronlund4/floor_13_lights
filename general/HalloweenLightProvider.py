from RandGenFixedLightProvider import RandGenFixedLightProvider
import random


class HalloweenLightProvider(RandGenFixedLightProvider):
    def __init__(self, colorIts=15, picks=50):
        super(HalloweenLightProvider, self).__init__([
            [252, 61, 3],
            [119, 3, 252]
        ], colorIts, picks)
