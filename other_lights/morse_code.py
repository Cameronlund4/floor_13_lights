import board
import neopixel
import time
import threading
import math
import os
import random
import sys


num_of_pixels = 300
colorIts = 1
pixels = neopixel.NeoPixel(board.D21, num_of_pixels,
                           brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)

morse_key = {
        'a' : '.-',
        'b' : '-...',
        'c' : '-.-.',
        'd' : '-..',
        'e' : '.',
        'f' : '..-.',
        'g' : '--.',
        'h' : '....',
        'i' : '..',
        'j' : '.---',
        'k' : '-.-',
        'l' : '.-..',
        'm' : '--',
        'n' : '-.',
        'o' : '---',
        'p' : '.--.',
        'q' : '--.-',
        'r' : '.-.',
        's' : '...',
        't' : '-',
        'u' : '..-',
        'v' : '...',
        'w' : '.--',
        'x' : '-..-',
        'y' : '-.--',
        'z' : '--..',
        '1' : '.----',
        '2' : '..---',
        '3' : '...--',
        '4' : '....-',
        '5' : '.....',
        '6' : '-....',
        '7' : '--...',
        '8' : '---..',
        '9' : '----.',
        '0' : '-----',
        '.' : '.-.-.-',
        ',' : '--..--',
        '?' : '..--..',
        '\'': '.----.',
        '!' : '-.-.--',
        '/' : '-..-.',
        '(' : '-.--.',
        ')' : '-.--.-',
        '&' : '.-...',
        ':' : '---...',
        ';' : '-.-.-.',
        '=' : '-...-',
        '+' : '.-.-.',
        '-' : '-....-',
        '_' : '..--.-',
        '"' : '.-..-.',
        '$' : '...-..-',
        '@' : '.--.-.'
        }


valColors = [
    [94, 8, 30],
    [181, 26, 58],
    [226, 71, 103],
    [228, 131, 151],
    [255, 0, 0]
]

def flash(duration, min_brightness, max_brightness):
    global pixels
    pixels.brightness = max_brightness
    time.sleep(duration)
    pixels.brightness = min_brightness


def morse_code(duration_between, message=""):
    # Duration of the actions and the duration of the waits between actions
    # Change dot_d for speed control of them all, dot_d is 1 time unit
    dot_d = 0.25
    dash_d = dot_d * 3
    same_let_gap = dot_d
    diff_let_gap = 2 * dot_d
    word_gap = 6 * dot_d

    # Defining Arguments and Constants for control of the flashing brightnesses
    if len(sys.argv) > 1:
        statement  = sys.argv[1].lower()
    else:
        statement = message.lower()
    global pixels
    upper_brightness = 1.0
    lower_brightness = 0.1
    pixels.brightness = lower_brightness
    time.sleep(duration_between)
    for char in statement:
        print("Showing: '{}' => {}".format(char, morse_key[char] if char is not ' ' else ' '))
        if char == ' ':
            time.sleep(word_gap)
            continue
        elif char not in morse_key:
            print("The character--", char, "--is not in the morse_key dictionary")
            print("\tIt was skipped")
            continue
        else:
            for action in morse_key[char]:
                if action == '.':
                    flash(dot_d, lower_brightness, upper_brightness)
                elif action == '-':
                    flash(dash_d, lower_brightness, upper_brightness)
                else:
                    print("ERROR: Read the wrong character in the morse_key dictionary")
                time.sleep(same_let_gap)
            time.sleep(diff_let_gap)
    pixels.brightness = lower_brightness
        

def loop_code():
    while True:
        morse_code(10, "instagram vinmino cameronlund4 ")


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


rainbow()

f = threading.Thread(target=loop_code)
f.setDaemon(True)
f.start()

newPixels = []
startInd = 0
while True:
    startInd = wrap(startInd, steps)
    nextInd = startInd
    for i in range(len(pixels)):
        pixels[i] = steps[nextInd]
        nextInd = wrap(nextInd+1, steps)
    pixels.show()
    startInd += 1
