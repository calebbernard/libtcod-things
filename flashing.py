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
    print rhythm
    return rhythm


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
    if rhythm[beatCount] == 1:
        numBars = random.randint(1,10)
        genColors(numBars)
    beatCount += 1
    beatCount %= 12

def main(key, mouse, timer):
    global colors, numBars
    everyTime(timer, .2, genBg)

    for x in range(numBars):
        paintBg(Coord((size_x / numBars) * x, 0), Coord((size_x / numBars) * (x + 1), size_y), colors[x])

def init():
    global rhythm
    rhythm = genRhythm()
    random.seed()
    genBg()

init()
coreLoop(key, mouse, main, size_x, size_y)
