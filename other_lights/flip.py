import board
import neopixel
import time
import threading
import math
import os
import random


num_of_pixels = 150
center_pixel = 76
branch_out_low = 30
branch_out_high = 50
colorIts = 15
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=0.1, auto_write=False, pixel_order=neopixel.GRB)

blueColors = [
    [59, 171, 253],
    [109, 193, 255],
    [178, 221, 255],
    [6, 205, 244],
    [34, 75, 139],
    [255, 255, 255]
]


def gradient(percent, colorA, colorB):
    color = [0, 0, 0]
    for i in range(3):
        color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
    return color


def gradientifyColors(steps, colors):
    steps = []
    colors.append(colors[0])
    print("Processing...")
    for i in range(len(colors)-1):
        for j in range(colorIts):
            perc = j/colorIts if i != 0 else 0
            steps.append(gradient(perc, colors[i], colors[i+1]))
    print("Done! Got", len(steps), "light instances!")
    return steps, colors


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


def rainy(steps, colors):
    global colorIts
    colorIts = 15
    for i in range(50):
        colors.append(random.choice(blueColors))
    return gradientifyColors(steps, colors)

def rainbow(steps, colors):
    global colorIts
    colorIts = 3
    for i in range(255, 0, -5):
        colors.append(wheel(i))
    return gradientifyColors(steps, colors)

steps1 = []
colors1 = []
steps2 = []
colors2 = []
# colors.extend([[255, 255, 0]] * 10)
# colors.extend([ [255, 0, 255]] * 10)
# steps = colors

steps1, colors1 = rainbow(steps1, colors1)
steps2, colors2 = rainy(steps2, colors2)

def wrap(index, length):
    if index >= len(length):
        return 0
    return index

def cloud(index, color, branch_out):
    distance = abs(index - center_pixel)
    if distance <= branch_out:
        return gradient((branch_out-(distance))/(branch_out), color, [255, 255, 255])
    else:
        return color

def randCloudDirection(branch_out, runs):
    if (runs % 5 == 0):
        if (branch_out == branch_out_high):
            return branch_out - 1
        elif (branch_out == branch_out_low):
            return branch_out + 1
        else:
            return branch_out + random.randint(-1,1)
    else:
        return branch_out

newPixels = []
leftStartInd1 = 0
rightStartInd1 = random.randint(0,len(steps1))
leftStartInd2 = 0
rightStartInd2 = random.randint(0,len(steps2))
branch_out_left = random.randint(branch_out_low, branch_out_high)
branch_out_right = random.randint(branch_out_low, branch_out_high)

while True:
    # Show rainbow
    for runs in range(30,350):
        branch_out_left = randCloudDirection(branch_out_left, runs)
        branch_out_right = randCloudDirection(branch_out_right, runs)
        steps = steps1
        leftStartInd1 = wrap(leftStartInd1, steps)
        rightStartInd1 = wrap(rightStartInd1, steps)

        # Draw left
            # Length: 300-center_pixel+1
            # Start at center_pixel+1
            # Go to num_of_pixels
        nextInd = leftStartInd1
        for i in range(num_of_pixels-1, center_pixel, -1):
            pixels[i] = cloud(i, steps[nextInd], branch_out_left)
            nextInd = wrap(nextInd+1, steps)
        nextInd = rightStartInd1
        # Draw right
        for i in range(0,center_pixel+1):
            pixels[i] = cloud(i, steps[nextInd], branch_out_right)
            nextInd = wrap(nextInd+1, steps)
            # Length: center_pixel
            # Start at center_pixel
            # Go to 0

        pixels.show()
        leftStartInd1 += 1
        rightStartInd1 += 1
    # Show rain
    for runs in range(5,55):
        branch_out_left = randCloudDirection(branch_out_left, runs)
        branch_out_right = randCloudDirection(branch_out_right, runs)
        steps = steps2
        leftStartInd2 = wrap(leftStartInd2, steps)
        rightStartInd2 = wrap(rightStartInd2, steps)

        # Draw left
            # Length: 300-center_pixel+1
            # Start at center_pixel+1
            # Go to num_of_pixels
        nextInd = leftStartInd2
        for i in range(num_of_pixels-1, center_pixel, -1):
            pixels[i] = cloud(i, steps[nextInd], branch_out_left)
            nextInd = wrap(nextInd+1, steps)
        nextInd = rightStartInd2
        # Draw right
        for i in range(0,center_pixel+1):
            pixels[i] = cloud(i, steps[nextInd], branch_out_right)
            nextInd = wrap(nextInd+1, steps)
            # Length: center_pixel
            # Start at center_pixel
            # Go to 0

        pixels.show()
        leftStartInd2 += 1
        rightStartInd2 += 1
