import libtcodpy as libtcod
import shelve

# To do:
# Very broken sometimes, fix
# Add any and last ports, fix JRO
# See about letting a command be on the same line as a loop label
# Make run button / hitbox bigger
# Sometimes lines highlight weird
# inter-node ports don't display their value

size_x = 144
size_y = 75
libtcod.console_set_custom_font('consolas8x8_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(size_x, size_y, 'TIS-99 (WIP Clone of TIS-100 by Zachtronics)', False)
libtcod.sys_set_fps(30)

class Node:
    def __init__(self, x, y, number, disabled, read):
        self.number = number
        self.x = x
        self.y = y
        self.disabled = disabled
        self.text = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.condensed = []
        self.cursorPosX = 0
        self.cursorPosY = 0
        self.cursorSec = 0
        self.acc = 0
        self.bak = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.read = read
        self.current = 0
        self.labels = {}
        self.failed = False
        self.last = -1

    def isTileMine(self, x, y):
        if x >= self.x + 1 and x <= self.x + 20 and y >= self.y + 1 and y <= self.y + 16:
            return True
        return False

    def click(self, x, y):
        relativeX = x - (self.x)
        relativeY = y - (self.y)
        self.goto(relativeX, relativeY)
        self.failed = False

    def goto(self, relativeX, relativeY):
        libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.black, flag=libtcod.BKGND_SET)
        if relativeY < 1:
            relativeY = 1
        elif relativeY > 15:
            relativeY = 15
        if self.text[relativeY - 1] == "":
            last = 0
            furtherDown = False
            # If there's text further down, then it's ok
            for z in range (relativeY, 15):
                if self.text[z] != "":
                    furtherDown = True
            # If there's no text further down, retreat to last line with text
            if not furtherDown:
                for z in range (relativeY):
                    if self.text[z] != "":
                        last = z
                self.cursorPosY = last + 1
            else: self.cursorPosY = relativeY
        else:
            self.cursorPosY = relativeY
        if relativeX < 1:
            relativeX = 1
        elif relativeX > 18:
            relativeX = 18
        else:
            if len(self.text[self.cursorPosY - 1]) <= relativeX - 1:
                self.cursorPosX = len(self.text[self.cursorPosY - 1]) + 1
            else:
                self.cursorPosX = relativeX

    def addLetter(self, char):
        char = char.upper()
        if len(self.text[self.cursorPosY - 1]) <= 17:
            libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.black, flag=libtcod.BKGND_SET)
            self.text[self.cursorPosY - 1] = (self.text[self.cursorPosY - 1][0:self.cursorPosX - 1]) + char + (self.text[self.cursorPosY - 1][self.cursorPosX - 1:])
            self.cursorPosX += 1

    def backspace(self):
        libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.black, flag=libtcod.BKGND_SET)
        if self.cursorPosX >= 2:
            self.text[self.cursorPosY - 1] = self.text[self.cursorPosY - 1][0:self.cursorPosX - 2] + self.text[self.cursorPosY - 1][self.cursorPosX - 1:]
            self.cursorPosX -= 1
        else:
            if self.cursorPosY >= 2:
                if (len(self.text[self.cursorPosY - 2]) + len(self.text[self.cursorPosY - 1])) <= 18:
                    self.cursorPosY -= 1
                    self.cursorPosX = len(self.text[self.cursorPosY - 1]) + 1
                    self.text[self.cursorPosY - 1] += self.text[self.cursorPosY]
                    for x in range (self.cursorPosY, 14):
                        self.text[x] = self.text[x+1]
                        self.text[14] = ""

    def newline(self):
        libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.black, flag=libtcod.BKGND_SET)
        if len(self.text[14]) == 0 and self.cursorPosY != 15:
            for x in reversed(range(self.cursorPosY + 1, 15)):
                self.text[x] = self.text[x-1]
            self.text[self.cursorPosY] = self.text[self.cursorPosY - 1][self.cursorPosX - 1:]
            self.text[self.cursorPosY - 1] = self.text[self.cursorPosY - 1][:self.cursorPosX - 1]
            self.cursorPosY += 1
            self.cursorPosX = 1

    def condense(self):
        self.condensed = []
        for line in self.text:
            if line != "" and line[0] != ';':
                self.condensed.append(line)

    def executeLine(self):
        global inputQueue, outQueue
        temp = None
        wait = False
        line = self.condensed[self.current]
        parse = line.split()
        if parse[0] == "MOV":
            if parse[1] == "UP":
                if self.read['up'] != "cin":
                    if nodes[self.read['up']].down == False:
                        wait = True
                    else:
                        temp = nodes[self.read['up']].down
                        nodes[self.read['up']].down = False
                else:
                    if len(inputQueue) > 0:
                        temp = inputQueue.pop()
                    else:
                        wait = True
            elif parse[1] == "DOWN":
                if nodes[self.read['down']].up == False:
                    wait = True
                else:
                    nodes[self.read['down']].up = False
                    temp = nodes[self.read['down']].up
            elif parse[1] == "LEFT":
                if nodes[self.read['left']].right == False:
                    wait = True
                else:
                    temp = nodes[self.read['left']].right
                    nodes[self.read['left']].right = False
            elif parse[1] == "RIGHT":
                if nodes[self.read['right']].left == False:
                    wait = True
                else:
                    temp = nodes[self.read['right']].left
                    nodes[self.read['right']].left = False
            elif parse[1] == "ACC":
                temp = self.acc
            elif parse[1] == "NIL":
                temp = 0
            elif int(parse[1]) >= -999 and int(parse[1]) <= 999:
                temp = int(parse[1])
            if not wait:
                if parse[2] == "UP":
                    if self.up == False:
                        self.up = temp
                    else:
                        wait = True
                elif parse[2] == "DOWN":
                    if self.read['down'] != "cout":
                        if self.down == False:
                            self.down = temp
                        else:
                            wait = True
                    else:
                        outQueue.insert(0, temp)
                elif parse[2] == "LEFT":
                    if self.left == False:
                        self.left = temp
                    else:
                        wait = True
                elif parse[2] == "RIGHT":
                    if self.right == False:
                        self.right = temp
                    else:
                        wait = True
                elif parse[2] == "ACC":
                    self.acc = temp
        elif parse[0] == "SAV":
            self.bak = self.acc
        elif parse[0] == "SWP":
            temp = self.bak
            self.bak = self.acc
            self.acc = temp
        elif parse[0] == "ADD":
            if parse[1] == "UP":
                if nodes[self.read['up']].down == False:
                    wait = True
                else:
                    self.acc += nodes[self.read['up']].down
                    nodes[self.read['up']].down = False
            elif parse[1] == "DOWN":
                if nodes[self.read['down']].up == False:
                    rwait = True
                else:
                    self.acc += nodes[self.read['down']].up
                    nodes[self.read['down']].up = False
            elif parse[1] == "LEFT":
                if nodes[self.read['left']].right == False:
                    wait = True
                else:
                    self.acc += nodes[self.read['left']].right
                    nodes[self.read['left']].right = False
            elif parse[1] == "RIGHT":
                if nodes[self.read['right']].left == False:
                    wait = True
                else:
                    self.acc += nodes[self.read['right']].left
                    nodes[self.read['right']].left = False
            elif parse[1] == "ACC":
                self.acc += self.acc
            elif parse[1] == "NIL":
                self.acc += 0
            elif int(parse[1]) >= -999 and int(parse[1]) <= 999:
                self.acc += int(parse[1])
        elif parse[0] == "SUB":
            if parse[1] == "UP":
                if nodes[self.read['up']].down == False:
                    wait = True
                else:
                    self.acc -= nodes[self.read['up']].down
                    nodes[self.read['up']].down = False
            elif parse[1] == "DOWN":
                if nodes[self.read['down']].up == False:
                    wait = True
                else:
                    self.acc -= nodes[self.read['down']].up
                    nodes[self.read['down']].up = False
            elif parse[1] == "LEFT":
                if nodes[self.read['left']].right == False:
                    wait = True
                else:
                    self.acc -= nodes[self.read['left']].right
                    nodes[self.read['left']].right = False
            elif parse[1] == "RIGHT":
                if nodes[self.read['right']].left == False:
                    wait = True
                else:
                    self.acc -= nodes[self.read['right']].left
                    nodes[self.read['right']].left = False
            elif parse[1] == "ACC":
                self.acc -= self.acc
            elif parse[1] == "NIL":
                self.acc -= 0
            elif int(parse[1]) >= -999 and int(parse[1]) <= 999:
                self.acc -= int(parse[1])
        elif parse[0] == "JMP":
            self.current = self.labels[parse[1]]
        elif parse[0] == "NEG":
            self.acc *= -1
        elif parse[0] == "JEZ":
            if self.acc == 0:
                self.current = self.labels[parse[1]]
        elif parse[0] == "JNZ":
            if self.acc != 0:
                self.current = self.labels[parse[1]]
        elif parse[0] == "JGZ":
            if self.acc > 0:
                self.current = self.labels[parse[1]]
        elif parse[0] == "JLZ":
            if self.acc < 0:
                self.current = self.labels[parse[1]]
        elif parse[0] == "JRO":
            self.current += int(parse[1])
        if self.acc >= 999:
            self.acc = 999
        if self.acc <= -999:
            self.acc = -999
        if self.bak >= 999:
            self.bak = 999
        if self.bak <= -999:
            self.bak = -999
        if not wait:
            self.current += 1
        if self.current == len(self.condensed):
            self.current = 0


    def validate(self):
        good = 0
        stores = ["UP", "DOWN", "LEFT", "RIGHT", "ACC", "NIL"]
        self.labels = {}
        if len(self.condensed) == 0:
            return True
        for line in range(len(self.condensed)):
            parts = self.condensed[line].split()
            if len(parts) != 0:
                if parts[0][-1] == ';':
                    self.labels[parts[0][:-1]] = line
        for line in range(len(self.condensed)):
            if self.condensed[line] == "":
                good += 1
            else:
                parts = self.condensed[line].split()
                if parts[0] == "MOV":
                    if len(parts) != 3:
                        break
                    else:
                        if (parts[1] in stores or (int(parts[1]) >= -999 and int(parts[1]) <= 999)) and parts[2] in stores:
                            "good here"
                            good += 1
                elif parts[0] == "SAV":
                    if len(parts) != 1:
                        break
                    else:
                        good += 1
                elif parts[0] == "NEG":
                    if len(parts) != 1:
                        break
                    else:
                        good += 1
                elif parts[0] == "SWP":
                    if len(parts) != 1:
                        break
                    else:
                        good += 1
                elif parts[0] == "ADD":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in stores or (int(parts[1]) >= -999 and int(parts[1]) <= 999):
                            good += 1
                elif parts[0] == "SUB":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in stores or (int(parts[1]) >= -999 and int(parts[1]) <= 999):
                            good += 1
                elif parts[0] == "JMP":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in self.labels:
                            good += 1
                elif parts[0] == "JEZ":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in self.labels:
                            good += 1
                elif parts[0][:-1] in self.labels:
                    good += 1
                elif parts[0] == "JNZ":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in self.labels:
                            good += 1
                elif parts[0] == "JGZ":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in self.labels:
                            good += 1
                elif parts[0] == "JLZ":
                    if len(parts) != 2:
                        break
                    else:
                        if parts[1] in self.labels:
                            good += 1
                elif parts[0] == "JRO":
                    if len(parts) != 2:
                        break
                    else:
                        if line + int(parts[1]) >= 0 and line + int(parts[1]) <= 15:
                            good += 1
        if good >= len(self.condensed):
            return True
        else:
            self.failed = True
            return False

    def draw(self):
        global executing
        box = [201, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 203, 205, 205, 205, 205, 205, 187,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 204,205,205,205,205,205,185,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 204,205,205,205,205,205,185,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 204,205,205,205,205,205,185,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 204,205,205,205,205,205,185,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                186, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 186,0,0,0,0,0,186,
                200, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 202, 205, 205, 205, 205, 205, 188,
                ]
        row = self.x
        col = self.y
        if self.failed:
            libtcod.console_set_default_foreground(0, libtcod.red)
        else:
            libtcod.console_set_default_foreground(0, libtcod.white)
        for char in box:
            libtcod.console_put_char(0, row, col, char, libtcod.BKGND_NONE)
            row += 1
            if row >= 27 + self.x:
                row = self.x
                col += 1
        if self.disabled:
            for z in range(13):
                libtcod.console_put_char(0, self.x + z + 4, self.y + 5, 176, libtcod.BKGND_NONE)
                libtcod.console_put_char(0, self.x + z + 4, self.y + 10, 176, libtcod.BKGND_NONE)
            libtcod.console_print_ex(0, self.x + 4, self.y + 7, libtcod.BKGND_NONE, libtcod.LEFT, "COMMUNICATION")
            libtcod.console_print_ex(0, self.x + 7, self.y + 8, libtcod.BKGND_NONE, libtcod.LEFT, "FAILURE")
        else:
            for y in range(15):
                for x in range(len(self.text[y])):
                    if not executing:
                        libtcod.console_set_default_foreground(0, libtcod.white)
                        libtcod.console_put_char(0, self.x + 1 + x, self.y + 1 + y, self.text[y][x], libtcod.BKGND_NONE)
                        libtcod.console_set_char_background(0, self.x + 1 + x, self.y + 1 + y, libtcod.black, flag=libtcod.BKGND_SET)
                    else:
                        if len(self.condensed) != 0:
                            if self.text[y] == self.condensed[self.current]:
                                libtcod.console_set_default_foreground(0, libtcod.black)
                                libtcod.console_set_char_background(0, self.x + 1 + x, self.y + 1 + y, libtcod.white, flag=libtcod.BKGND_SET)
                                libtcod.console_put_char(0, self.x + 1 + x, self.y + 1 + y, self.text[y][x], libtcod.BKGND_NONE)
                            else:
                                libtcod.console_set_char_background(0, self.x + 1 + x, self.y + 1 + y, libtcod.black, flag=libtcod.BKGND_SET)
                                libtcod.console_set_default_foreground(0, libtcod.white)
                                libtcod.console_put_char(0, self.x + 1 + x, self.y + 1 + y, self.text[y][x], libtcod.BKGND_NONE)
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, self.x + 29, self.y + 5, "\32", libtcod.BKGND_NONE) # right
        libtcod.console_put_char(0, self.x - 3, self.y + 10, "\33", libtcod.BKGND_NONE) # left
        libtcod.console_put_char(0, self.x + 15, self.y - 3, "\30", libtcod.BKGND_NONE) # up
        libtcod.console_put_char(0, self.x + 7, self.y + 19, "\31", libtcod.BKGND_NONE) # down
        if self.right != False:
            libtcod.console_print_ex(0, self.x + 27, self.y + 6, libtcod.BKGND_NONE, libtcod.LEFT, str(self.right))
            for x in range(len(str(self.right)) + 1, 5):
                libtcod.console_put_char(0, self.x + 27, self.y + 6, " ", libtcod.BKGND_NONE)
        else:
            libtcod.console_print_ex(0, self.x + 27, self.y + 6, libtcod.BKGND_NONE, libtcod.LEFT, "     ")
        if self.left != False:
            libtcod.console_print_ex(0, self.x -5, self.y + 6, libtcod.BKGND_NONE, libtcod.LEFT, str(self.left))
        else:
            libtcod.console_print_ex(0, self.x -5, self.y + 6, libtcod.BKGND_NONE, libtcod.LEFT, "     ")
        if self.up != False:
            libtcod.console_print_ex(0, self.x + 16, self.y - 3, libtcod.BKGND_NONE, libtcod.LEFT, str(self.up))
        else:
            libtcod.console_print_ex(0, self.x + 16, self.y - 3, libtcod.BKGND_NONE, libtcod.LEFT, "     ")
        if self.down != False:
            libtcod.console_print_ex(0, self.x + 8, self.y + 19, libtcod.BKGND_NONE, libtcod.LEFT, str(self.down))
        else:
            libtcod.console_print_ex(0, self.x + 8, self.y + 19, libtcod.BKGND_NONE, libtcod.LEFT, "     ")

        if not self.disabled:
            libtcod.console_set_default_foreground(0, libtcod.Color(150,150,150))
            libtcod.console_print_ex(0, self.x + 22, self.y + 1, libtcod.BKGND_NONE, libtcod.LEFT, "ACC")
            libtcod.console_print_ex(0, self.x + 22, self.y + 4, libtcod.BKGND_NONE, libtcod.LEFT, "BAK")
            libtcod.console_set_default_foreground(0, libtcod.white)
            libtcod.console_print_ex(0, self.x + 22, self.y + 2, libtcod.BKGND_NONE, libtcod.LEFT, str(self.acc))
            libtcod.console_print_ex(0, self.x + 22, self.y + 5, libtcod.BKGND_NONE, libtcod.LEFT, str(self.bak))
        if timeElapsed % 1 > .5 and focus == self.number and not self.disabled:
            libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.white, flag=libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_background(0, self.x + self.cursorPosX, self.y + self.cursorPosY, libtcod.black, flag=libtcod.BKGND_SET)

def clear_bg():
    for x in range(size_x):
        for y in range(size_y):
            libtcod.console_set_char_background(0, x, y, libtcod.black, flag=libtcod.BKGND_SET)

def saveState():
    f = open("load.txt", "r")
    program = f.readline()
    f.close()
    f = shelve.open(program, "n")
    f['nodes'] = nodes
    f.close()

def loadState():
    global nodes
    f = open("load.txt", "r")
    program = f.readline()
    f.close()
    f = shelve.open(program, "r")
    nodes = f['nodes']
    f.close()

def drawConsoleBox(x, y):
    libtcod.console_put_char(0, x, y, 201, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 6, y, 187, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x, y + 31, 204, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 6, y + 31, 185, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 6, y + 32, 186, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x, y + 32, 186, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x, y + 33, 200, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 6, y + 33, 188, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 1, y + 33, 205, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 2, y + 33, 205, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 3, y + 33, 205, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 4, y + 33, 205, libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x + 5, y + 33, 205, libtcod.BKGND_NONE)
    for z in range(5):
        libtcod.console_put_char(0, x+z+1, y, 205, libtcod.BKGND_NONE)
        libtcod.console_put_char(0, x+z+1, y+31, 205, libtcod.BKGND_NONE)
    for z in range(30):
        libtcod.console_put_char(0, x, y+z+1, 186, libtcod.BKGND_NONE)
        libtcod.console_put_char(0, x+6, y+z+1, 186, libtcod.BKGND_NONE)

def initNodes():
    global nodes, focus
    focus = -1
    nodes = []
    try:
        loadState()
    except:
        number = 0
        row_y = [7, 29, 51]
        row_x = [15, 47, 79, 111]
        for y in row_y:
            for x in row_x:
                read = {}
                disabled = False
                if y != row_y[0]:
                    read['up'] = number - 4
                else:
                    read['up'] = None
                if x != row_x[0]:
                    read['left'] = number - 1
                else:
                    read['left'] = None
                if y != row_y[len(row_y) - 1]:
                    read['down'] = number + 4
                else:
                    read['down'] = None
                if x != row_x[len(row_x) - 1]:
                    read['right'] = number + 1
                else:
                    read['right'] = None
                if number == 1:
                    read['up'] = "cin"
                if number == 10:
                    read['down'] = 'cout'
                nodes.append(Node(x, y, number, disabled, read))
                number += 1
    drawConsoleBox(2, 17)
    libtcod.console_print_ex(0, 53, 2, libtcod.LEFT, libtcod.BKGND_NONE, "Input")
    libtcod.console_put_char(0, 55, 4, "\31", libtcod.BKGND_NONE)
    libtcod.console_print_ex(0, 84, 72, libtcod.LEFT, libtcod.BKGND_NONE, "Output")
    libtcod.console_print_ex(0, 4, 63, libtcod.LEFT, libtcod.BKGND_NONE, "Run")

def run_program():
    global key, mouse, inputQueue, outQueue, executing
    executing = True
    done = False
    validateCount = 0
    for node in nodes:
        node.current = 0
        node.condense()
    for node in nodes:
        if node.validate():
            validateCount += 1
    if validateCount == 12:
        libtcod.console_put_char(0, 3, 49, ">", libtcod.BKGND_NONE)
        input = ""
        inputQueue = []
        outQueue = []
        history = []
        historyStart = 0
        done = False
        while executing:
            clear_bg()
            libtcod.console_set_char_background(0, 5, 61, libtcod.Color(0,255,0), flag=libtcod.BKGND_SET)
            libtcod.console_set_char_background(0, mouse.cx, mouse.cy, libtcod.Color(50,50,50), flag=libtcod.BKGND_SET)
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
            for x in range(len(input), 4):
                libtcod.console_print_ex(0, 4+x, 49, libtcod.LEFT, libtcod.BKGND_NONE, ' ')
            libtcod.console_print_ex(0, 4, 49, libtcod.LEFT, libtcod.BKGND_NONE, input)
            if mouse.lbutton_pressed:
                if mouse.cx == 5 and mouse.cy == 61:
                    executing = False
                    libtcod.console_print_ex(0, 3, 49, libtcod.LEFT, libtcod.BKGND_NONE, "     ")
                    for y in range(30):
                        libtcod.console_print_ex(0, 3, 18 + y, libtcod.LEFT, libtcod.BKGND_NONE, "     ")
                    libtcod.console_set_char_background(0, 5, 61, libtcod.Color(255,0,0), flag=libtcod.BKGND_SET)
                    for node in nodes:
                        node.acc = 0
                        node.bak = 0
                        node.up = False
                        node.down = False
                        node.right = False
                        node.left = False
                    break
            if chr(key.c) >= "0" and chr(key.c) <= "9":
                if len(input) < 3 or (len(input) < 4 and input[0] == '-'):
                    input += chr(key.c)
            elif chr(key.c) == '-':
                if len(input) == 0 or input[0] != '-':
                    input = '-' + input
                else:
                    input = input[1:]
            elif key.vk == libtcod.KEY_ESCAPE:
                saveState()
                return False
            elif key.vk == libtcod.KEY_BACKSPACE:
                input = input[:-1]
            elif key.vk == libtcod.KEY_ENTER:
                if input != "":
                    inputQueue.insert(0, int(input))
                    if len(history) <= 29:
                        history.append(">" + input)
                    else:
                        history[historyStart] = ">" + input
                        historyStart += 1
                        if historyStart >= 29:
                            historyStart -= 29
                    input = ""
            for y in range(29):
                for x in range(len(input), 4):
                    libtcod.console_print_ex(0, 4+x, 19 + y, libtcod.LEFT, libtcod.BKGND_NONE, ' ')
            for index in range(len(history)):
                trueIndex = index + historyStart
                if trueIndex >= 29:
                    trueIndex -= 29
                libtcod.console_print_ex(0, 3, 18 + index, libtcod.LEFT, libtcod.BKGND_NONE, history[trueIndex])
            for node in nodes:
                if len(node.condensed) > 0:
                    node.executeLine()
            if len(outQueue) > 0:
                for n in range(len(outQueue)):
                    if len(history) <= 29:
                        history.append(" " + str(outQueue.pop()))
                    else:
                        history[historyStart] = " " + str(outQueue.pop())
                        historyStart += 1
                        if historyStart >= 29:
                            historyStart -= 29
            for element in nodes:
                element.draw()
            libtcod.console_flush()





def play_game():
    global key, mouse, nodes, timeElapsed, focus, executing
    player_action = None
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    while not libtcod.console_is_window_closed():
        executing = False
        clear_bg()
        libtcod.console_set_char_background(0, 5, 61, libtcod.Color(255,0,0), flag=libtcod.BKGND_SET)
        libtcod.console_set_char_background(0, mouse.cx, mouse.cy, libtcod.Color(50,50,50), flag=libtcod.BKGND_SET)
        timeElapsed = libtcod.sys_elapsed_seconds()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        if mouse.lbutton_pressed:
            if mouse.cx == 5 and mouse.cy == 61:
                run_program()
            else:
                success = False
                for num in range(len(nodes)):
                    x = mouse.cx
                    y = mouse.cy
                    if nodes[num].isTileMine(x, y):
                        focus = num
                        success = True
                        nodes[focus].click(x, y)
                if success == False:
                    focus = -1
        if key.vk == libtcod.KEY_ESCAPE:
            saveState()
            return 0
        if focus != -1:
            if key.vk == libtcod.KEY_BACKSPACE:
                nodes[focus].backspace()
            if key.vk == libtcod.KEY_ENTER:
                nodes[focus].newline()
            if key.vk == libtcod.KEY_UP:
                    nodes[focus].goto(nodes[focus].cursorPosX, nodes[focus].cursorPosY - 1)
            if key.vk == libtcod.KEY_DOWN:
                    nodes[focus].goto(nodes[focus].cursorPosX, nodes[focus].cursorPosY + 1)
            if key.vk == libtcod.KEY_LEFT:
                    nodes[focus].goto(nodes[focus].cursorPosX - 1, nodes[focus].cursorPosY)
            if key.vk == libtcod.KEY_RIGHT:
                    nodes[focus].goto(nodes[focus].cursorPosX + 1, nodes[focus].cursorPosY)
            if chr(key.c) >= chr(32) and chr(key.c) <= chr(126):
                    nodes[focus].addLetter(chr(key.c))
        for element in nodes:
            element.draw()
        libtcod.console_flush()

def init():
    initNodes()
    focus = -1

init()
play_game()
