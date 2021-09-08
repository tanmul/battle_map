import os
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import random
import math

WIDTH, HEIGHT = 1920, 1080
canvas_WIDTH, canvas_HEIGHT = 1575, 1080

canvas_center = [canvas_WIDTH/2, canvas_HEIGHT/2]
# WIDTH, HEIGHT = 2240, 1260
ids = []

drag_data = {"x": 0, "y": 0, "item": None}
rot_data = {"xy": 0, "center": 0, "id": None}

heroes = []

class Spawner(Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        self.config( bg ='white', width=355, height=HEIGHT/2)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)

        heroes = ['Swig', 'Hardin', 'Silene', 'Bones', 'Liniear', 'Hikou', 'Jeff']
        hero_var = StringVar(self)
        hero_var.set(heroes[0])

        self.hero_chooser = OptionMenu(self, hero_var, *heroes)
        self.hero_chooser.grid(row = 0, column = 0, sticky='nsew')

        self.hero_spawner = Button(self, text='Spawn Hero', command=lambda:self.spawn_hero(canvas, hero_var))
        self.hero_spawner.grid(row=0, column = 1, sticky = "nsew")

        self.enemy_spawner = Button(self, text='Spawn Enemy', command=lambda: self.spawn_enemy(canvas))
        self.enemy_spawner.grid(row=1, column = 1, sticky = "nsew", columnspan=2)

        shapes = ['Rectangle', 'Triangle', 'Oval']
        shape_var = StringVar(self)
        shape_var.set(shapes[0])

        self.shape_chooser = OptionMenu(self, shape_var, *shapes)
        self.shape_chooser.grid(row=2, column=0, sticky='nsew', columnspan=2)

        self.sphere_checker = Button(self, text='Check Radius', command=lambda: self.check_radius(canvas, shape_var))
        self.sphere_checker.grid(row=3, column = 1, sticky = "nsew", columnspan=2)


    def spawn_hero(self, canvas, hero_var):
        hero_models_dir = "player_models\\"
        hero_color_dict = {
            'Swig': 'Swig_assasin_wizard.png',
            'Hardin': 'cyan',
            'Silene': 'silene_leech.png',
            'Bones': 'darkblue',
            'Hikou': 'snow',
            'Liniear': 'darkgrey',
            'Jeff': 'Jeff.png'
        }
        x = random.randrange(0, 1575)
        y = random.randrange(0, 1080)
        chosen_hero = hero_var.get()
        if(chosen_hero == 'Swig' or chosen_hero == 'Jeff' or chosen_hero == 'Silene'):
            full_hero_path = os.path.join(hero_models_dir, hero_color_dict[chosen_hero])
            hero_pic = Image.open(full_hero_path)
            resized_hero = hero_pic.resize((45, 55), Image.ANTIALIAS)
            resized_hero.save((chosen_hero+"_resized.png"), "png")
            heroes.append(PhotoImage(file=(chosen_hero+'_resized.png')))
            canvas.battle_map_hero = heroes[-1]
            ids.append(canvas.create_image(canvas_center[0], canvas_center[1], image=heroes[-1], tags=("character",)))
        else:
            ids.append(canvas.create_oval(x, y, x+30, y+30, outline='black', fill=hero_color_dict[chosen_hero], tags=("character",)))

    def spawn_enemy(self, canvas):
        x = random.randrange(0, 1575)
        y = random.randrange(0, 1080)
        ids.append(canvas.create_oval(x, y, x+30, y+30, outline='black', fill='red', tags=("character",)))

    def check_radius(self, canvas, shape_var):
        shape_color_dict = {
            'Rectangle': 'blueviolet',
            'Triangle': 'darkgreen',
            'Oval': 'orangered',
        }
        chosen_shape = shape_var.get()
        if(chosen_shape == 'Oval'):
            ids.append(canvas.create_oval(705, 450, 705+(45*8), 450+(45*8), outline=shape_color_dict[chosen_shape], width=4, tags=("circle",)))
        elif chosen_shape == 'Rectangle':
            rectangle = canvas.create_rectangle(647, 450, 647+(45*1), 450+(45*20), outline=shape_color_dict[chosen_shape], width=4, tags=("rectangle",))
            coords = canvas.coords(rectangle)
            x0, y0, x2, y2 = coords[0], coords[1], coords[2], coords[3]
            x1 = x2
            y1 = y0
            x3 = x0
            y3 = y2
            xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
            canvas.delete(rectangle)
            rect_poly = canvas.create_polygon(xy, fill='', outline='blueviolet', width=4, tags=("rectangle",))
            center = [(int)((x2 + x0)/2), (int)((y2 + y0)/2)]
            rot_data['id'] = rect_poly
            rot_data['xy'] = xy
            rot_data['center'] = center

            print(rot_data['xy'])
            print(rot_data['center'])

def main():
    xy = []
    center = []
    root = Tk()
    root.geometry("1920x1080")
    root.title('EGCS BATTLE MAP!')
    root.resizable(False, False)
    root.config(bg='black')
    battle_mat_file = Image.open("The_Campgrounds_.jpg")
    resized = battle_mat_file.resize((1575, HEIGHT), Image.ANTIALIAS)
    resized.save("resized.ppm", "ppm")
    battle_mat_bg = PhotoImage(file = 'resized.ppm')
    battle_mat = tkinter.Canvas(root, bg='white', width=1575, height=HEIGHT, bd=-2, highlightthickness=0)
    battle_mat.place(x = 0, y = 0)
    battle_mat.create_image(0, 0, image=battle_mat_bg, anchor='nw')
    battle_map_hero = []

    def create_grid(event):
        w = battle_mat.winfo_width()  # Get current width of canvas
        h = battle_mat.winfo_height()  # Get current height of canvas
        battle_mat.delete('grid_line')  # Will only remove the grid_line
        for i in range(0, w, 45):
            battle_mat.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 45):
            battle_mat.create_line([(0, i), (w, i)], tag='grid_line')
    battle_mat.bind('<Configure>', create_grid)

    spawner = Spawner(root, battle_mat)
    spawner.place(x = 1575, y = 0)


    # frame2 = Frame(root, bg='blue')
    # frame2.place(x = 1575, y = 540)

    def calculate_newxy_center(objectid):
        coords = battle_mat.coords(objectid)
        x0, y0, x1, y1, x2, y2, x3, y3 = coords[0], coords[1], coords[2], coords[3], coords[4], coords[5], coords[6], coords[7]
        xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
        center = [(int)((x2 + x0) / 2), (int)((y2 + y0) / 2)]
        rot_data['xy'] = xy
        rot_data['center'] = center

    def drag_start(event):
        """Begining drag of an object"""
        # record the item and its location
        drag_data["item"] = battle_mat.find_closest(event.x, event.y)[0]
        if(drag_data['item'] >= 61):
            battle_mat.addtag_withtag("drag",drag_data['item'])
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def drag_stop(event):
        """End drag of an object"""
        # reset the drag information
        if drag_data['item'] == rot_data['id']:
            calculate_newxy_center(drag_data['item'])
        drag_data["item"] = None
        drag_data["x"] = 0
        drag_data["y"] = 0
        battle_mat.dtag("drag", "drag")

    def drag(event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - drag_data["x"]
        delta_y = event.y - drag_data["y"]

        # move the object the appropriate amount
        # self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        battle_mat.move("drag", delta_x, delta_y)

        # record the new position
        drag_data["x"] = event.x
        drag_data["y"] = event.y



    def delete_char(event):
        # record the item and its location
        object_id = battle_mat.find_closest(event.x, event.y)[0]
        if object_id > 60:
            battle_mat.delete(object_id)

    def getangle(event):
        dx = battle_mat.canvasx(event.x) - rot_data['center'][0]
        dy = battle_mat.canvasy(event.y) - rot_data['center'][1]
        try:
            return complex(dx, dy) / abs(complex(dx, dy))
        except ZeroDivisionError:
            return 0.0  # cannot determine angle

    def press(event):
        # calculate angle at start point
        global start
        start = getangle(event)

    def motion(event):
        # calculate current angle relative to initial angle
        global start
        angle = getangle(event) / start
        offset = complex(rot_data['center'][0], rot_data['center'][1])
        newxy = []
        xy = rot_data['xy']
        for x, y in xy:
            v = angle * (complex(x, y) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)
        battle_mat.coords(rot_data['id'], *newxy)


    battle_mat.tag_bind("character", "<ButtonPress-1>", drag_start)
    battle_mat.tag_bind("character", "<ButtonRelease-1>", drag_stop)
    battle_mat.tag_bind("character", "<B1-Motion>", drag)
    battle_mat.tag_bind("character", "<Button-3>", delete_char)
    battle_mat.tag_bind("rectangle", "<ButtonPress-1>", drag_start)
    battle_mat.tag_bind("rectangle", "<ButtonRelease-1>", drag_stop)
    battle_mat.tag_bind("rectangle", "<B1-Motion>", drag)
    battle_mat.tag_bind("rectangle", "<Button-3>", delete_char)
    battle_mat.tag_bind("circle", "<ButtonPress-1>", drag_start)
    battle_mat.tag_bind("circle", "<ButtonRelease-1>", drag_stop)
    battle_mat.tag_bind("circle", "<B1-Motion>", drag)
    battle_mat.tag_bind("circle", "<Button-3>", delete_char)

    battle_mat.tag_bind("rectangle", "<Button-2>", press)
    battle_mat.tag_bind("rectangle", "<B2-Motion>", motion)
    root.mainloop()

if __name__ == '__main__':
    main()