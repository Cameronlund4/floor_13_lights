import board
import neopixel
import time
import threading
import math
import os


num_of_pixels = 300
colorIts = 5
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)


def gradient(percent, colorA, colorB):
    color = [0, 0, 0]
    for i in range(3):
        color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
    return color


def set_color(colorA, colorB):
    global pixels
    for i in range(colorIts):
        perc = i/colorIts if i != 0 else 0
        print(perc)
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
    # if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
    return (r, g, b)

colors = []

for i in range(255, 0, -5):
    colors.append(wheel(i))
colors.append(colors[0]);

steps = []

print("Processing...")
for i in range(len(colors)-1):
    for j in range(colorIts):
        perc = j/colorIts if i != 0 else 0
        steps.append(gradient(perc, colors[i], colors[i+1]))

print("Done! Got",len(colors),"light instances!")

def wrap(index, length):
    if index >= len(length):
        return 0;
    return index;

newPixels = []
startInd = 0
while True:
    startInd = wrap(startInd, steps)
    print("New loop!")
    nextInd = startInd
    for i in range(len(pixels)):
        pixels[i] = steps[nextInd]
        nextInd = wrap(nextInd+i, steps)
    pixels.show()
    steps += 1