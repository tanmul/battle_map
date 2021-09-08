from tkinter import *

import math

c = Canvas(width=500, height=500)
c.pack()

# a square
# xy = [(50, 50), (150, 50), (150, 150), (50, 150)]
rectangle_item = c.create_rectangle(50, 50, 150, 150)
x0, y0, x2, y2 = c.coords(rectangle_item)
c.delete(rectangle_item)
# x0 = 50
# y0 = 50
# x2 = 150
# y2 = 150
x1 = x2
y1 = y0
x3 = x0
y3 = y2
xy = [(x0, y0), (x1,y1), (x2,y2), (x3,y3)]

rect_poly = c.create_polygon(xy)

center = [x2-x0, y2-y0]

# coords = c.coords(rectangle_item)

# Now to create tuples of coordinates
# xy = [(coords[0],coords[1]), (coords[2],coords[1]), (coords[2],coords[3]), (coords[2],coords[1])]
# c.delete(rectangle_item)
# rect_poly = c.create_polygon(xy, fill='black')
# print(c.coords(rect_poly))
#
# # That's how we get the relative center of the object
# print(coords)
# print(coords[2]-coords[0], coords[3]-coords[1])

def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0 # cannot determine angle

def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)

def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    offset = complex(center[0], center[1])
    newxy = []
    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    c.coords(rect_poly, *newxy)

c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)

mainloop()