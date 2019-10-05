import board
import neopixel
import time
import threading
import math
import os


num_of_pixels = 300
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)


def gradient(percent, colorA, colorB):
    color = [0, 0, 0]
    for i in range(3):
        color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
    return color


def set_color(colorA, colorB):
    global pixels
    for i in range(50):
        perc = i/50 if i != 0 else 0
        print(perc)
        pixels.fill(gradient(perc, colorB, colorA))
        pixels.show()


while True:
    set_color([255, 127, 0], [255, 255, 0])
    time.sleep(0.25)
    set_color([255, 255, 0], [0, 255, 0])
    time.sleep(0.25)
    set_color([0, 255, 0], [0, 0, 255])
    time.sleep(0.25)
    set_color([0, 0, 255], [75, 0, 130])
    time.sleep(0.25)
    set_color([75, 0, 130], [148, 0, 211])
    time.sleep(0.25)
    set_color([148, 0, 211], [255, 0, 0])
    time.sleep(0.25)
    set_color([255, 0, 0], [255, 127, 0])
    time.sleep(0.25)
