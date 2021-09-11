import os
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import random
import math

WIDTH, HEIGHT = 1920, 1080
canvas_WIDTH, canvas_HEIGHT = (int)(WIDTH/1.215), HEIGHT
canvas_center = [canvas_WIDTH/2, canvas_HEIGHT/2]
HERO_WIDTH, HERO_HEIGHT = 45, 55

ids = []

drag_data = {"x": 0, "y": 0, "item": None}
rot_data = {"xy": 0, "center": 0, "id": None}

hero_data = {}
duplicate_hero_data = {}
last_resized = 0
heroes = []
main_heroes = []
paint_var = False

double_click_flag = False

class Spawner(Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        self.config( bg ='white', width=(WIDTH-canvas_WIDTH), height=HEIGHT/2)
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


        self.paint_button_1 = Radiobutton(self, text='Pen Up', variable=paint_var, value=False)
        self.paint_button_2 = Radiobutton(self, text='Pen Down', variable=paint_var, value=True)


    def spawn_hero(self, canvas, hero_var):
        hero_models_dir = "player_models\\"
        hero_color_dict = {
            'Swig': 'Swig_assasin_wizard.png',
            'Hardin': 'cyan',
            'Silene': 'silene_leech.png',
            'Bones': 'bones_boob_lady.png',
            'Hikou': 'snow',
            'Liniear': 'darkgrey',
            'Jeff': 'Jeff.png'
        }
        x = random.randrange(0, canvas_WIDTH)
        y = random.randrange(0, canvas_HEIGHT)
        chosen_hero = hero_var.get()
        if chosen_hero == 'Swig' or chosen_hero == 'Jeff' or chosen_hero == 'Silene' or chosen_hero == 'Bones':
            full_hero_path = os.path.join(hero_models_dir, hero_color_dict[chosen_hero])
            hero_pic = Image.open(full_hero_path)
            resized_hero = hero_pic.resize((HERO_WIDTH, HERO_HEIGHT), Image.ANTIALIAS)
            resized_hero_path = chosen_hero+"_resized.png"
            resized_hero.save(resized_hero_path, "png")
            heroes.append(PhotoImage(file=(chosen_hero+'_resized.png')))
            canvas.battle_map_hero = heroes[-1]
            hero_object_id = canvas.create_image(canvas_center[0], canvas_center[1], image=heroes[-1], tags=("character",))
            data_dict = {hero_object_id :
                {
                'hero_name': chosen_hero,
                'hero_path': full_hero_path,
                'base_width': HERO_WIDTH,
                'base_height': HERO_HEIGHT,
                'current_width': HERO_WIDTH,
                'current_height': HERO_HEIGHT
                }
            }
            ids.append(hero_object_id)
            if chosen_hero not in main_heroes:
                main_heroes.append(chosen_hero)
                hero_data.update(data_dict)
            else:
                duplicate_hero_data.update(data_dict)

            print(hero_data)
            print(duplicate_hero_data)
        else:
            ids.append(canvas.create_oval(x, y, x+30, y+30, outline='black', fill=hero_color_dict[chosen_hero], tags=("character",)))


    def spawn_enemy(self, canvas):
        x = random.randrange(0, canvas_WIDTH)
        y = random.randrange(0, canvas_HEIGHT)
        ids.append(canvas.create_oval(x, y, x+30, y+30, outline='black', fill='red', tags=("character",)))

    def check_radius(self, canvas, shape_var):
        shape_color_dict = {
            'Rectangle': 'blueviolet',
            'Triangle': 'darkgreen',
            'Oval': 'orangered',
        }
        chosen_shape = shape_var.get()
        if(chosen_shape == 'Oval'):
            ids.append(canvas.create_oval((canvas_WIDTH/2 - (45*4)), (canvas_HEIGHT/2 - (45*4)), (canvas_WIDTH/2 + (45*8)), (canvas_HEIGHT/2 + (45*8)), outline=shape_color_dict[chosen_shape], width=4, tags=("circle",)))
        elif chosen_shape == 'Rectangle':
            rectangle = canvas.create_rectangle(647, 450, 647+(45*1), 450+(45*20), outline=shape_color_dict[chosen_shape], width=4, tags=("rectangle",))
            coords = canvas.coords(rectangle)
            x0, y0, x2, y2 = coords[0], coords[1], coords[2], coords[3]
            x1, y1, x3, y3 = x2, y0, x0, y2
            xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
            canvas.delete(rectangle)
            rect_poly = canvas.create_polygon(xy, fill='', outline='blueviolet', width=4, tags=("rectangle",))
            center = [(int)((x2 + x0)/2), (int)((y2 + y0)/2)]
            rot_data['id'] = rect_poly
            rot_data['xy'] = xy
            rot_data['center'] = center

    def is_paiting(self, canvas):


def main():
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title('EGCS BATTLE MAP!')
    root.resizable(False, False)
    root.config(bg='black')
    battle_map_file = Image.open("The_Campgrounds_.jpg")
    resized = battle_map_file.resize((canvas_WIDTH, canvas_HEIGHT), Image.ANTIALIAS)
    resized.save("resized.ppm", "ppm")
    battle_map_bg = PhotoImage(file = 'resized.ppm')
    battle_map = tkinter.Canvas(root, bg='white', width=canvas_WIDTH, height=HEIGHT, bd=-2, highlightthickness=0)
    battle_map.place(x = 0, y = 0)
    battle_map_backdrop =battle_map.create_image(0, 0, image=battle_map_bg, anchor='nw')

    def create_grid(event):
        w = battle_map.winfo_width()  # Get current width of canvas
        h = battle_map.winfo_height()  # Get current height of canvas
        battle_map.delete('grid_line')  # Will only remove the grid_line
        for i in range(0, w, 45):
            battle_map.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 45):
            battle_map.create_line([(0, i), (w, i)], tag='grid_line')
    battle_map.bind('<Configure>', create_grid)

    spawner = Spawner(root, battle_map)
    spawner.place(x = canvas_WIDTH, y = 0)

    def calculate_newxy_center(objectid):
        coords = battle_map.coords(objectid)
        x0, y0, x1, y1, x2, y2, x3, y3 = coords[0], coords[1], coords[2], coords[3], coords[4], coords[5], coords[6], coords[7]
        new_xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
        new_center = [(int)((x2 + x0) / 2), (int)((y2 + y0) / 2)]
        rot_data['xy'] = new_xy
        rot_data['center'] = new_center

    def drag_start(event):
        global last_resized
        """Begining drag of an object"""
        # record the item and its location
        drag_data["item"] = battle_map.find_closest(event.x, event.y)[0]
        if(drag_data['item'] > 1):
            battle_map.addtag_withtag("drag",drag_data['item'])
            battle_map.dtag(last_resized, "resizable")
            battle_map.addtag_withtag("resizable", drag_data['item'])

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
        battle_map.dtag("drag", "drag")


    def drag(event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - drag_data["x"]
        delta_y = event.y - drag_data["y"]

        # move the object the appropriate amount
        # self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        battle_map.move("drag", delta_x, delta_y)

        # record the new position
        drag_data["x"] = event.x
        drag_data["y"] = event.y


    def paint_obstacle(event, actionables: list):
        if paint_var == True:
            print('painting')
        else:
            print('not painting')
        closest_object = battle_map.find_closest(event.x, event.y)[0]
        if 'drag' not in battle_map.gettags(closest_object) and 'obstacle' not in battle_map.gettags(closest_object):
            color = 'tan4'
            x1, y1 = (event.x-1), (event.y-1)
            x2, y2 = (event.x+1), (event.y+1)
            battle_map.create_oval(x1, y1, x2, y2, fill = color, outline = color, width=7, tags = ('obstacle',))

    def erase_obstacle(event):
        closest_object = battle_map.find_closest(event.x, event.y)[0]
        if 'obstacle' in battle_map.gettags(closest_object):
            battle_map.delete(closest_object)

    def delete_char(event):
        object_id = battle_map.find_closest(event.x, event.y)[0]
        if object_id > 1 and 'obstacle' not in battle_map.gettags(object_id):
            battle_map.delete(object_id)
            try:
                hero_data.pop(object_id)
            except KeyError:
                duplicate_hero_data.pop(object_id)
    def resize_image(hero_path, char_name, new_width, new_height, x, y):
        hero_pic = Image.open(hero_path)
        resized_hero = hero_pic.resize((new_width, new_height), Image.ANTIALIAS)
        resized_hero_path = char_name + "_new_resized.png"
        resized_hero.save(resized_hero_path, "png")
        heroes.append(PhotoImage(file=resized_hero_path))
        battle_map.battle_map_hero = heroes[-1]
        hero = battle_map.create_image(x, y, image=heroes[-1], tags=("character", "resizable",))
        ids.append(hero)
        return hero

    def enlarge(event):
        global hero_data, duplicate_hero_data, last_resized
        closest_object = battle_map.find_withtag('resizable')[-1]
        print(f"Making object {closest_object} bigger.")
        current_char = ''
        image_width = 0
        image_height = 0
        hero_path = ''
        is_dup = False
        data_dict = hero_data
        if closest_object in duplicate_hero_data:
            data_dict = duplicate_hero_data
            is_dup = True
        current_char = data_dict[closest_object]['hero_name']
        hero_path = data_dict[closest_object]['hero_path']
        image_width = data_dict[closest_object]['current_width']
        image_height = data_dict[closest_object]['current_height']

        new_width = image_width*2
        new_height = image_height*2

        if closest_object in ids:
            battle_map.delete(closest_object)
            ids.remove(closest_object)
            new_hero_object_id = resize_image(hero_path, current_char, new_width, new_height, event.x, event.y)
            data_dict[new_hero_object_id] = data_dict.pop(closest_object)
            data_dict[new_hero_object_id]['current_width'] = new_width
            data_dict[new_hero_object_id]['current_height'] = new_height
            if is_dup:
                duplicate_hero_data = data_dict
            else:
                hero_data = data_dict
            last_resized = new_hero_object_id

    def shrink(event):
        global hero_data, duplicate_hero_data, last_resized
        closest_object = battle_map.find_withtag('resizable')[-1]
        print(f"Making object {closest_object} bigger.")
        current_char = ''
        image_width = 0
        image_height = 0
        hero_path = ''
        is_dup = False
        data_dict = hero_data
        if closest_object in duplicate_hero_data:
            data_dict = duplicate_hero_data
            is_dup = True
        current_char = data_dict[closest_object]['hero_name']
        hero_path = data_dict[closest_object]['hero_path']
        image_width = data_dict[closest_object]['current_width']
        image_height = data_dict[closest_object]['current_height']

        new_width = (int)(image_width / 2)
        new_height = (int)(image_height / 2)

        if closest_object in ids:
            battle_map.delete(closest_object)
            ids.remove(closest_object)
            new_hero_object_id = resize_image(hero_path, current_char, new_width, new_height, event.x, event.y)
            data_dict[new_hero_object_id] = data_dict.pop(closest_object)
            data_dict[new_hero_object_id]['current_width'] = new_width
            data_dict[new_hero_object_id]['current_height'] = new_height
            if is_dup:
                duplicate_hero_data = data_dict
            else:
                hero_data = data_dict
            last_resized = new_hero_object_id

    def getangle(event):
        dx = battle_map.canvasx(event.x) - rot_data['center'][0]
        dy = battle_map.canvasy(event.y) - rot_data['center'][1]
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
        battle_map.coords(rot_data['id'], *newxy)

    movable_tags = ['character', 'rectangle', 'circle']
    for tag in movable_tags:
        battle_map.tag_bind(tag, "<ButtonPress-1>", drag_start)
        battle_map.tag_bind(tag, "<ButtonRelease-1>", drag_stop)
        battle_map.tag_bind(tag, "<B1-Motion>", drag)

    deletable_tags = movable_tags+['obstacle']
    for tag in deletable_tags:
        battle_map.tag_bind(tag, "<Button-3>", delete_char)

    rotatable_tags = ['rectangle']
    for tag in rotatable_tags:
        battle_map.tag_bind(tag, "<Button-2>", press)
        battle_map.tag_bind(tag, "<B2-Motion>", motion)

    resizable_tags = ['character']

    battle_map.bind('<B1-Motion>', lambda event: paint_obstacle(event, movable_tags+rotatable_tags))
    battle_map.bind('<B3-Motion>', erase_obstacle)
    root.bind('<Up>', enlarge)
    root.bind('<Down>', shrink)

    root.mainloop()

if __name__ == '__main__':
    main()