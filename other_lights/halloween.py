import board
import neopixel
import time
import threading
import math
import os
import random


num_of_pixels = 300
colorIts = 1
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)
valColors = [
    [252, 61, 3],
    [119, 3, 252]
    ]


def gradient(percent, colorA, colorB):
    color = [0, 0, 0]
    for i in range(3):
        color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
    return color


def gradientifyColors():
    global steps
    global colors
    steps = []
    colors.append(colors[0])
    #print("Processing...")
    for i in range(len(colors)-1):
        for j in range(colorIts):
            perc = j/colorIts if i != 0 else 0
            steps.append(gradient(perc, colors[i], colors[i+1]))
    #print("Done! Got", len(steps), "light instances!")


def set_color(colorA, colorB):
    global pixels
    for i in range(colorIts):
        perc = i/colorIts if i != 0 else 0
        #print(perc)
        pixels.fill(gradient(perc, colorA, colorB))
        pixels.show()


def wheel(pos):
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


def rainbow():
    global colorIts
    global colors
    colorIts = 3
    for i in range(255, 0, -5):
        colors.append(wheel(i))
    gradientifyColors()


def valentines():
    global colorIts
    global colors
    colorIts = 15
    for i in range(50):
        colors.append(random.choice(valColors))
    gradientifyColors()


def slowValentines():
    global colorIts
    global colors
    colorIts = 75
    for i in range(len(valColors)):
        colors.append(valColors[i])
    for i in range(0, len(valColors), -1):
        colors.append(valColors[i])
    gradientifyColors()


def binaryGradient(color1, color2):
    global colorIts
    global colors
    colorIts = 30
    colors.append(color1)
    colors.append(color2)
    gradientifyColors()


def wrap(index, length):
    if index >= len(length):
        return 0
    return index


steps = []

colors = []
# colors.extend([[255, 255, 0]] * 10)
# colors.extend([ [255, 0, 255]] * 10)
# steps = colors

valentines()

newPixels = []
startInd = 0
while True:
    startInd = wrap(startInd, steps)
    nextInd = startInd
    for i in range(14, len(pixels)):
        pixels[i] = steps[nextInd]
        nextInd = wrap(nextInd+1, steps)
    for j in range(15):
        pixels[j] = gradient((j+1)/15, [255, 255, 255], steps[nextInd])
        nextInd = wrap(nextInd+1, steps)
    pixels.show()
    startInd += 1
