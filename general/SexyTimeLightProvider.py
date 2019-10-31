from RandGenFixedLightProvider import RandGenFixedLightProvider
import random


class SexyTimeLightProvider(RandGenFixedLightProvider):
    def __init__(self, colorIts=15, picks=50):
        super(SexyTimeLightProvider, self).__init__([
            [94, 8, 30],
            [181, 26, 58],
            [226, 71, 103],
            [228, 131, 151],
            [255, 0, 0]
        ], colorIts, picks)
