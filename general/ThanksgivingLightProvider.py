from RandGenFixedLightProvider import RandGenFixedLightProvider
from FixedLightProvider import FixedLightProvider
import random


class ThanksgivingLightProvider(FixedLightProvider):
    def __init__(self):
        super(ThanksgivingLightProvider, self).__init__([
                [255, 0, 0] * 10,
                [230, 230, 230] * 10,
                [0, 0, 255] * 10
                ])
