from math import sqrt
from random import randint
from time import sleep
from tkinter import Canvas, Tk

class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    def to_hex(self):
        red = hex(self.red)[2:]
        green = hex(self.green)[2:]
        blue = hex(self.blue)[2:]
        if len(red) == 1:
            red = '0' + red
        if len(green) == 1:
            green = '0' + green
        if len(blue) == 1:
            blue = '0' + blue
        return '#' + red + green + blue

WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW = Color(255, 255, 0)
BLACK = Color(0, 0, 0)

class Sprite:
    def __init__(self):
        self.time = 0
    def tick(self):
        self.time += 1

class Picture(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.shapes = []
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def add_shape(self, shape):
        self.shapes.append(shape)
    def get_color_at(self, row, col):
        for shape in reversed(self.shapes):
            color = shape.get_color_at(row, col)
            if color:
                return color
        return WHITE
    def tick(self):
        self.time += 1
        for shape in self.shapes:
            shape.tick()

class Point(Sprite):
    def __init__(self, row, col, color):
        Sprite.__init__(self)
        self.row = row
        self.col = col
        self.color = color
    def get_color_at(self, row, col):
        if row == self.row and col == self.col:
            return self.color
        else:
            return None

class Rectangle(Sprite):
    def __init__(self, row, col, height, width, color):
        Sprite.__init__(self)
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.color = color
    def get_color_at(self, row, col):
        if self.row <= row <= self.row + self.height and self.col <= col <= self.col + self.width:
            return self.color
        else:
            return None

class Circle(Sprite):
    def __init__(self, row, col, radius, color):
        Sprite.__init__(self)
        self.row = row
        self.col = col
        self.radius = radius
        self.color = color
    def get_color_at(self, row, col):
        if sqrt((self.row - row) ** 2 + (self.col - col) ** 2) <= self.radius:
            return self.color
        else:
            return None

class Star(Point):
    def __init__(self, row, col, color, frequency):
        Point.__init__(self, row, col, color)
        self.frequency = frequency
    def get_color_at(self, row, col):
        if self.time % self.frequency != 0:
            return Point.get_color_at(self, row, col)
        else:
            return None

class Ship(Sprite):
    def __init__(self, row, col):
        Sprite.__init__(self)
        self.row = row
        self.col = col
    def get_color_at(self, row, col):
        self.col = 110 - (self.time % 240)
        if row == self.row - 2 and col == self.col + 1:
            return Color(245, 247, 58)
        elif row == self.row - 1 and self.col - 1 <= col <= self.col + 5:
            return BLACK
        elif row == self.row and self.col <= col <= self.col + 5:
            return BLACK
        else:
            return None

class Cloud(Sprite):
    def __init__(self, row, col, color):
        Sprite.__init__(self)
        self.row = row
        self.init_col = col
        self.col = 0
        self.color = color
    def get_color_at(self, row, col):
        self.col = self.init_col + (2 * (self.time % 400)) - 50
        if row == self.row - 2 and self.col + 7 <= col <= self.col + 11:
            return self.color
        elif row == self.row - 1 and self.col + 4 <= col <= self.col + 13:
            return self.color
        elif row == self.row and self.col <= col <= self.col + 9:
            return self.color
        elif row == self.row + 1 and self.col + 6 <= col <= self.col + 15:
            return self.color
        else:
            return None

class LightHouse(Sprite):
    def __init__(self, row, col, frequency):
        Sprite.__init__(self)
        self.row = row
        self.col = col
        self.frequency = frequency
        self.parts = [
            Rectangle(self.row - 24, self.col - 3, 4, 6, RED),
            Rectangle(self.row - 19, self.col - 3, 4, 6, WHITE),
            Rectangle(self.row - 14, self.col - 3, 4, 6, RED),
            Rectangle(self.row - 9, self.col - 3, 4, 6, WHITE),
            Rectangle(self.row - 4, self.col - 3, 4, 6, RED),
        ]
        self.light = Rectangle(self.row - 27, self.col - 2, 2, 4, YELLOW)
    def get_color_at(self, row, col):
        for part in self.parts:
            color = part.get_color_at(row, col)
            if color is not None:
                if col > self.col + 1:
                    return Color(color.red // 2, color.green // 2, color.blue // 2)
                else:
                    return color
        if self.light.get_color_at(row, col):
            step = self.time % self.frequency
            if step < self.frequency / 2:
                rg = int(255 * step / (self.frequency / 2))
            else:
                rg = int(255 * (self.frequency - step) / (self.frequency / 2))
            return Color(rg, rg, 0)
        return None

def create_picture():
    pic = Picture(100, 100)
    pic.add_shape(Rectangle(0, 0, 60, 100, Color(27, 1, 71)))
    pic.add_shape(Rectangle(60, 0, 40, 100, Color(31, 7, 148)))
    for i in range(15):
        rg = randint(220, 250)
        b = randint(180, 220)
        pic.add_shape(Star(randint(1, 50), randint(0, 100), Color(rg, rg, b), randint(20, 100)))
    pic.add_shape(Circle(25, 15, 10, Color(242, 235, 220)))
    for i in range(3):
        gray = randint(100, 200)
        pic.add_shape(Cloud(randint(1, 30), randint(0, 100), Color(gray, gray, gray)))
    pic.add_shape(Ship(60, 50))
    pic.add_shape(Rectangle(75, 0, 7, 45, BLACK))
    pic.add_shape(LightHouse(80, 41, 6))
    return pic

class Viewer:
    def __init__(self, picture):
        self.picture = picture
        self.scale = 4
        self.canvas_items = set()
        self.tk_root = Tk()
        self.canvas = Canvas(self.tk_root, width=(self.scale * self.picture.get_width()), height=(self.scale * self.picture.get_height()))
        self.canvas.pack()
        self.canvas.focus_set()
    def animate(self):
        while True:
            sleep(0.5)
            self.update()
            self.canvas.pack()
            self.canvas.update()
            self.picture.tick()
    def update(self):
        for item in self.canvas_items:
            self.canvas.delete(item)
        for y in range(self.picture.get_height()):
            row = y - 1
            for x in range(self.picture.get_width()):
                col = x - 1
                if 0 <= row < self.picture.get_height() and 0 <= col < self.picture.get_width():
                    color = self.picture.get_color_at(row, col)
                    item = self.canvas.create_rectangle(self.scale * x, self.scale * y, self.scale * (x + 1), self.scale * (y + 1), fill=color.to_hex(), outline='')
                    self.canvas_items.add(item)
    def display(self):
        self.tk_root.after(0, self.animate)
        self.tk_root.mainloop()

def main():
    pic = create_picture()
    viewer = Viewer(pic)
    viewer.display()

if __name__ == '__main__':
    main()
