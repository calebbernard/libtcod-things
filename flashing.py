import sys
sys.path.append("..")
from library import *
import random

size_x = 30
size_y = 30
font = '../dejavu16x16_gs_tc.png'
title = 'Flashing'
fps = 30
mouse = libtcod.Mouse()
key = libtcod.Key()
startWin(font, size_x, size_y, title, fps)

colorBand = 100
colorOffset = 100

def genColors(num):
    global colors
    colors = []
    for x in range(num):
        colors.append(color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

def genBg():
    global numBars
    numBars = random.randint(1,10)
    genColors(numBars)

def main(key, mouse, timer):
    global colors, numBars
    everyTime(timer, 2, genBg)

    for x in range(numBars):
        paintBg(Coord((size_x / numBars) * x, 0), Coord((size_x / numBars) * (x + 1), size_y), colors[x])

def init():
    random.seed()
    genBg()

init()
coreLoop(key, mouse, main, size_x, size_y)
