import sys
sys.path.append("..")
from library import *
import random

size_x = 30
size_y = 30
font = '../consolas8x8_gs_tc.png'
title = 'Reverse Hour'
fps = 30
mouse = libtcod.Mouse()
key = libtcod.Key()
startWin(font, size_x, size_y, title, fps)

class Car:
    def __init__(self, color, orientation, direction, moveType, size, pos, solid):
        self.color = color
        self.orientation = orientation
        self.direction = direction
        self.moveType = moveType
        self.size = size
        self.pos = pos
        self.solid = solid
        self.held = False

    def draw(self):
        coords = self.getCoords()
        for element in coords:
            setBg(element.x, element.y, self.color)

    def getCoords(self):
        coords = []
        if self.orientation == "horizontal":
            for x in range(self.size):
                coords.append(Coord(self.pos.x + x, self.pos.y))
        else:
            for y in range(self.size):
                coords.append(Coord(self.pos.x, self.pos.y + y))
        return coords

    def move(self):
        if not self.held:
            if self.moveType == "mobile":
                if self.orientation == "horizontal":
                    if self.collision(Coord(self.pos.x - 1, self.pos.y)) and self.collision(Coord(self.pos.x + self.size, self.pos.y)):
                        return
                    if self.direction == "up/left":
                        if not self.collision(Coord(self.pos.x - 1, self.pos.y)):
                            self.pos.x -= 1
                        else:
                            self.direction = "down/right"
                            self.move()
                    else:
                        if not self.collision(Coord(self.pos.x + self.size, self.pos.y)):
                            self.pos.x += 1
                        else:
                            self.direction = "up/left"
                            self.move()
                elif self.orientation == "vertical":
                    if self.collision(Coord(self.pos.x, self.pos.y - 1)) and self.collision(Coord(self.pos.x, self.pos.y + self.size)):
                        return
                    if self.direction == "up/left":
                        if not self.collision(Coord(self.pos.x, self.pos.y - 1)):
                            self.pos.y -= 1
                        else:
                            self.direction = "down/right"
                            self.move()
                    else:
                        if not self.collision(Coord(self.pos.x, self.pos.y + self.size)):
                            self.pos.y += 1
                        else:
                            self.direction = "up/left"
                            self.move()
            elif self.moveType == "spinner":
                car = self.collision(self.pos)
                if car:
                    if car.orientation == "horizontal":
                        car.orientation = "vertical"
                    else:
                        car.orientation = "horizontal"


    def collision(self, pos):
        if pos.x < 0 or pos.x > size_x - 1:
            return True
        if pos.y < 0 or pos.y > size_y - 1:
            return True
        for car in cars:
            if car != self:
                carCoords = car.getCoords()
                for element in carCoords:
                    if element.x == pos.x and element.y == pos.y and car.solid == True:
                        if not car.held:
                            if car.orientation == self.orientation:
                                if car.direction == "up/left":
                                    car.direction = "down/right"
                                else:
                                    car.direction = "up/left"
                        return car
        return False


def moveCars():
    global cars
    for car in cars:
        car.move()
    if checkFinish():
        return True

def checkFinish():
    heroCoords = cars[0].getCoords()
    finishCoords = cars[1].getCoords()
    for item in range(len(heroCoords)):
        if heroCoords[item].x == finishCoords[item].x and heroCoords[item].y == heroCoords[item].y:
            return True

def main(key, mouse, timer):
    global cars
    for item in cars:
        item.draw()
    if mouse.lbutton_pressed:
        for item in cars:
            carCoords = item.getCoords()
            for coordinate in carCoords:
                if mouse.cx == coordinate.x and mouse.cy == coordinate.y:
                    item.held = not item.held
    if everyTime(timer, .25, moveCars):
        print "Complete!"
        return True


def init():
    global cars
    cars = []
    cars.append(Car(color(255,0,0), "horizontal", "up/left", "mobile", 3, Coord(25, 25), True))
    cars.append(Car(color(0,255,0), "horizontal", "up/left", "static", 3, Coord(10, 25), False))
    cars.append(Car(color(255,255,0), "horizontal", "down/right", "mobile", 2, Coord(15, 25), True))
    cars.append(Car(color(255,255,0), "vertical", "up/left", "mobile", 15, Coord (20, 15), True))
    cars.append(Car(color(0,0,255), "vertical", "up/left", "spinner", 1, Coord(25, 25), False))


init()
coreLoop(key, mouse, main, size_x, size_y, color(10,10,10), "highlight", color(80,80,80))
