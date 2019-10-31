from RandGenFixedLightProvider import RandGenFixedLightProvider
import random


class OceanLightProvider(RandGenFixedLightProvider):
    def __init__(self, colorIts=15, picks=50):
        super(OceanLightProvider, self).__init__([
            [0, 0, 255],
            [59, 171, 253],
            [109, 193, 255],
            [178, 221, 255],
            [6, 205, 244],
            [34, 75, 139],
            [255, 255, 255]
        ], colorIts, picks)
