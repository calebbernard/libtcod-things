import sys
sys.path.append("..")
from library import *
import random

size_x = 30
size_y = 30
font = '../dejavu16x16_gs_tc.png'
title = 'Flashing'
fps = 60
mouse = libtcod.Mouse()
key = libtcod.Key()
startWin(font, size_x, size_y, title, fps)

colorBand = 100
colorOffset = 100

def genRhythm():
    groups = 4
    beats = 3
    rhythm = []
    group = []
    for n in range(beats):
        group.append(random.randint(0,1))
    for m in range(groups):
        for n in range(beats):
            rhythm.append(group[n])
    return [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def genColors(num):
    global colors
    colors = []
    for x in range(num):
        colors.append(color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

def genBg():
    global numBars, beatCount
    try:
        beatCount
    except:
        beatCount = 0
    try:
        numBars
    except:
        numBars = random.randint(1,10)
        genColors(numBars)
    print rhythm[beatCount]
    if rhythm[beatCount] == 1:
        numBars = random.randint(1,10)
        genColors(numBars)
    else:
        for color in colors:
            v = .8
            if color.r > 64:
                r_mul = .95
            else:
                r_mul = 1.25
            if color.g > 50:
                g_mul = .95
            else:
                g_mul = 1.25
            if color.b > 50:
                b_mul = .95
            else:
                b_mul = 1.25
            color.r = max(0, min(int(color.r * r_mul), 255))
            color.g = max(0, min(int(color.g * g_mul), 255))
            color.b = max(0, min(int(color.b * b_mul), 255))
    beatCount += 1
    beatCount %= len(rhythm)

def main(key, mouse, timer):
    global colors, numBars
    everyTime(timer, .05, genBg)

    for x in range(numBars):
        paintBg(Coord((size_x / numBars) * x, 0), Coord((size_x / numBars) * (x + 1), size_y), colors[x])

def init():
    global rhythm
    rhythm = genRhythm()
    random.seed()
    genBg()

init()
coreLoop(key, mouse, main, size_x, size_y)
