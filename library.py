import libtcodpy as libtcod

'''
non-blocking input:
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
blocking input:
    key = libtcod.console_wait_for_keypress(True)
'''

def startWin(font, size_x, size_y, title, fps):
    libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(size_x, size_y, title, False)
    libtcod.sys_set_fps(fps)

def setBg(x, y, color):
    libtcod.console_set_char_background(0, x, y, color, flag=libtcod.BKGND_SET)

def color(R,G,B):
    return libtcod.Color(R,G,B)

def paintBg(top_left, bot_right, color):
    for x in range(top_left.x, bot_right.x):
        for y in range(top_left.y, bot_right.y):
            setBg(x, y, color)

def putString(x, y, string, color):
    libtcod.console_set_default_foreground(0, color)
    libtcod.console_print_ex(0, x, y, libtcod.BKGND_NONE, libtcod.LEFT, string)

def putChar(x, y, char, color):
    libtcod.console_set_default_foreground(0, color)
    libtcod.console_put_char(0, x, y, char, libtcod.BKGND_NONE)

def mouseHover(highlight, newColor, mouse):
    if not highlight:
        setBg(mouse.cx, mouse.cy, newColor)
    else:
        currRed = libtcod.console_get_char_background(0,mouse.cx, mouse.cy).r
        currGreen = libtcod.console_get_char_background(0,mouse.cx, mouse.cy).g
        currBlue = libtcod.console_get_char_background(0,mouse.cx, mouse.cy).b
        if currRed >= 128:
            red = currRed - newColor.r
        else:
            red = currRed + newColor.r
        if currGreen >= 128:
            green = currGreen - newColor.g
        else:
            green = currGreen + newColor.g
        if currBlue >= 128:
            blue = currBlue - newColor.b
        else:
            blue = currBlue + newColor.b
        setBg(mouse.cx, mouse.cy, color(red, green, blue))

def getElapsedSeconds():
    return libtcod.sys_elapsed_seconds()

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def coreLoop(key, mouse, function, size_x, size_y):
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        paintBg(Coord(0,0), Coord(size_x, size_y), color(170,40,40))
        timer = getElapsedSeconds()
        function(key, mouse, timer)
        mouseHover(True, color(25,25,25), mouse)
        if key.vk == libtcod.KEY_ESCAPE:
            return 0
        libtcod.console_flush()

def everyTime(timer, time, function):
    global lastSeconds
    try:
        lastSeconds
    except:
        lastSeconds = 0
    if lastSeconds + time < timer:
        lastSeconds = timer
        function()
'''

class boxBorder:
    def __init__(self, borderStyle, borderColor):
        self.borderStyle = borderStyle
        self.borderColor = borderColor
        self.calcTiles()

    def calcTiles(self):
        if self.borderStyle == "Single":
            self.tiles = {"horizontal": 196, "vertical": 179, "topRight": 191, "topLeft": 218, "bottomRight": 217, "bottomLeft": 192}
        elif self.borderStyle == "Double":
            self.tiles = {"horizontal": 205, "vertical": 186, "topRight": 187, "topLeft": 201, "bottomRight": 188, "bottomLeft": 200}
        else:
            self.tiles = {"horizontal": ' ', "vertical": ' ', "topRight": ' ', "topLeft": ' ', "bottomRight": ' ', "bottomLeft": ' '}

class Box:
    def __init__(self, topLeft, botRight, border, bgStyle, bgColor, bgBorder):
        self.topLeft = topLeft
        self.botRight = botRight
        self.border = border
        self.bgStyle = bgStyle
        self.bgColor = bgColor
        self.bgBorder = bgBorder

    def draw(self):
        if self.bgStyle != None:
            self.fill()
        if self.borderStyle != None:
            self.border()

    def fill(self):
        # Fill
        topLeft = Coord(self.topLeft.x, self.topLeft.y)
        botRight = Coord(self.botRight.x, self.botRight.y)
        if self.bgBorder == False:
            topLeft.x += 1
            topLeft.y += 1
            botRight.x -= 1
            botRight.y -= 1
        paintBg(topLeft, botRight, self.bgColor)
'''
