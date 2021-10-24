import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw
import json


# GLOBAL CONSTANTS
# Need to be set
WIDTH, HEIGHT = 1260, 720
BLOCK_SIZE = 30
SIZES = {'Tiny': 0.5, 'Small': 1, 'Medium': 1, 'Large': 2, 'Huge': 3, 'Gargantuan': 4}
background_color = 'gray13'

# Calculated automatically
canvas_WIDTH, canvas_HEIGHT = WIDTH, (int)(3*HEIGHT/4)
canvas_center = [canvas_WIDTH/2, canvas_HEIGHT/2]
HERO_WIDTH, HERO_HEIGHT = BLOCK_SIZE, BLOCK_SIZE+10

# Global variables, need to be accessed between frames and canvas
# Create a better way to hold ids for everything on the board at any point
ids = []
drag_data = {"x": 0, "y": 0, "item": None}
rot_data = {"xy": 0, "center": 0, "id": None}

hero_data = {}
duplicate_hero_data = {}
enemy_data = {}
last_resized = 0
heroes = []
main_heroes = []
is_painting = False

class Menu(Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        frame_width, frame_height = WIDTH, (int)(HEIGHT/4)
        self.config(bg=background_color, width=frame_width, height=frame_height)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='row')

        self.battlemap_bg_label = ttk.Label(self, text='Find a picture to use for the battlemap:', background=background_color)
        self.battlemap_bg_label.grid(row=0, column=1, sticky='EW')
        self.battlemap_bg_button = ttk.Button(self, text='Browse', command=lambda: choose_bm_bg(self, canvas))
        self.battlemap_bg_button.grid(row=0, column=2, sticky='EW')

        # resolutions = ['1280 by 720', '1920 by 1080', '2560 by 1440']
        # screen_resolution = StringVar(self)
        # self.battlemap_application_size = ttk.Label(self, text = 'Choose a resolution?', background = background_color)
        # self.battlemap_application_size.grid(row=1, column=1, sticky='EW', columnspan = 2)
        # self.battemap_resolution = ttk.OptionMenu(self, screen_resolution, resolutions[0], *resolutions, command=)
        # self.battemap_resolution.grid(row=1, column=2, sticky='EW')

        players = ['Swig', 'Hardin', 'Silene', 'Bones']
        hero_var = StringVar(self)
        self.hero_chooser = ttk.OptionMenu(self, hero_var, players[0], *players)
        self.hero_chooser.grid(row=0, column=3, sticky='EW')

        self.hero_spawner = ttk.Button(self, text='Spawn Hero', command=lambda: spawn_hero(self,canvas, hero_var))
        self.hero_spawner.grid(row=0, column=4, sticky='EW')

        self.size_options = list(SIZES.keys())
        self.size_var = StringVar(self)
        self.enemy_size_choice = ttk.OptionMenu(self, self.size_var, self.size_options[2], *self.size_options)
        self.enemy_size_choice.grid(row=1, column=3, sticky='EW')

        self.enemy_spawner = ttk.Button(self, text='Spawn Enemy',
                                        command=lambda: spawn_enemy(self,canvas, self.size_var.get()))
        self.enemy_spawner.grid(row=1, column=4, sticky='EW')

        width_var = StringVar(self)
        height_var = StringVar(self)
        self.width_label = ttk.Label(self, text='Spell width/radius (ft)', background=background_color)
        self.width_label.grid(row=2, column=3, sticky='EW', ipadx=5)
        self.entry_width = ttk.Entry(self, textvariable=width_var)
        self.entry_width.grid(row=2, column=4, sticky='EW')
        self.height_label = ttk.Label(self, text='Spell height/radius (ft)', background=background_color)
        self.height_label.grid(row=3, column=3, sticky='EW', ipadx=5)
        self.entry_height = ttk.Entry(self, textvariable=height_var)
        self.entry_height.grid(row=3, column=4, sticky='EW')

        shapes = ['Rectangle', 'Triangle', 'Oval']
        shape_var = StringVar(self)
        self.shape_chooser = ttk.OptionMenu(self, shape_var, shapes[0], *shapes)
        self.shape_chooser.grid(row=4, column=3, sticky='EW')

        self.sphere_checker = ttk.Button(self, text='Check Radius', command=lambda: check_radius(self,canvas, shape_var, width_var, height_var))
        self.sphere_checker.grid(row=4, column=4, sticky='EW')

        paint_var = BooleanVar()
        paint_var.set(False)
        s = ttk.Style()
        s.configure('Wild.TRadiobutton', background=background_color)
        self.paint_button_1 = ttk.Radiobutton(self, text='Pen Up', variable=paint_var, value=False,
                                              command=lambda: is_painting(self, paint_var.get()), style='Wild.TRadiobutton')
        self.paint_button_1.grid(row=5, column=3, sticky='NSEW')
        self.paint_button_2 = ttk.Radiobutton(self, text='Pen Down', variable=paint_var, value=True,
                                              command=lambda: is_painting(self,paint_var.get()), style='Wild.TRadiobutton')
        self.paint_button_2.grid(row=5, column=4, sticky='NSEW')

        self.player_label = ttk.Label(self, text='Character', anchor = 'center', borderwidth = 2, background=background_color)
        self.flying_label = ttk.Label(self, text='Current Height', anchor='center', borderwidth=2, background=background_color)
        self.health_label = ttk.Label(self, text='Current Health', anchor = 'center', borderwidth = 2, background=background_color)
        self.class_label = ttk.Label(self, text='Class', anchor = 'center', borderwidth = 2, background=background_color)
        self.player_label.grid(row=0, column=5, sticky='EW')
        self.flying_label.grid(row=0, column=6, sticky='EW')
        self.health_label.grid(row=0, column=7, sticky='EW')

        row_count = 1
        for hero in players:
            original_sprite_dir = 'player_models\\original\\sprites\\'
            hero_path = os.path.join(original_sprite_dir, hero + '_original.png')
            image = Image.open(hero_path)
            resized = image.resize((30, 35), Image.ANTIALIAS)
            resized.save('temp.png', "png")
            final_im = PhotoImage(file='temp.png')
            self.char_label = ttk.Label(self)
            self.char_label.image = final_im
            self.char_label.config(image=final_im, background=background_color)
            self.char_label.grid(row=row_count, column=5)
            self.flying_entry = ttk.Entry(self)
            self.health_entry = ttk.Entry(self)
            self.flying_entry.grid(row=row_count, column=6, sticky='NSEW')
            self.health_entry.grid(row=row_count, column=7, sticky='NSEW')
            row_count += 1


        def choose_bm_bg(self, canvas):
            global battlemap_bg
            try:
                filename = askopenfilename(filetypes=[('Image Files', ['*.jpeg', "*.jpg", "*.png", "*.img"])])
                if filename is not None:
                    image = Image.open(filename)
                    resized = image.resize((canvas_WIDTH, canvas_HEIGHT), Image.ANTIALIAS)
                    resized.save('battlemap_bg.png', "png")
                    canvas.config(width=0, height =0)
                    canvas.update()
                    battlemap_bg = PhotoImage(file='battlemap_bg.png')
                    canvas.create_image(0, 0, image=battlemap_bg, anchor='nw', tags=('bg',))
                    canvas.config(width=canvas_WIDTH, height=HEIGHT)
                    canvas.update()
            except AttributeError:
                print("No image input")
                self.master.destroy()

        def is_painting(self, value):
            global is_painting
            is_painting = value

        def spawn_hero(self, canvas, hero_var):
            original_hero_image_dir = "player_models\\original\\sprites\\"
            base_hero_sprites_dir = "player_models\\base_sprites\\"
            duplicate_sprite_dir = "player_models\\original\\duplicates\\"
            chosen_hero = hero_var.get()
            base_sprite_file = chosen_hero + "_resized.png"
            base_sprite_path = base_hero_sprites_dir + base_sprite_file
            print("Base sprite path: ", base_sprite_path)
            original_image_path = os.path.join(original_hero_image_dir, (chosen_hero + "_original.png"))
            if chosen_hero not in main_heroes:
                print('First time spawning ', chosen_hero)
                image = Image.open(original_image_path)
                base_sprite = image.resize((HERO_WIDTH, HERO_HEIGHT), Image.ANTIALIAS)
                base_sprite.save(base_sprite_path, "png")
                heroes.append(PhotoImage(file=base_sprite_path))
            else:
                print("Creating a duplicate of ", chosen_hero)
                dup_hero_file = chosen_hero + '_duplicate_resized.png'
                dup_hero_image_path = os.path.join(base_hero_sprites_dir, dup_hero_file)
                dup_original_file = chosen_hero + '_duplicate.png'
                dup_original_path = os.path.join(duplicate_sprite_dir, dup_original_file)
                # Check if we need to create the dupe sprite or if we can load a previous
                if dup_hero_file not in os.listdir(base_hero_sprites_dir):
                    image = Image.open(dup_original_path)
                    resized = image.resize((HERO_WIDTH, HERO_HEIGHT), Image.ANTIALIAS)
                    resized.save(dup_hero_image_path, "png")
                original_image_path = dup_original_path
                heroes.append(PhotoImage(file=dup_hero_image_path))
            canvas.battle_map_hero = heroes[-1]
            hero_object_id = canvas.create_image(canvas_center[0], canvas_center[1], image=heroes[-1],tags=("character",))
            data_dict = {hero_object_id:
                {
                    'hero_name': chosen_hero,
                    'hero_path': original_image_path,
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

        def spawn_enemy(self, canvas, size_var):
            enemy_object_id = canvas.create_oval(canvas_center[0], canvas_center[1], canvas_center[0] + (BLOCK_SIZE * SIZES[size_var]),
                                          canvas_center[1] + (BLOCK_SIZE * SIZES[size_var]), outline='black', fill='red',
                                          tags=("character",))
            enemy_data_dict = {enemy_object_id:
               {
                    'enemy_size': size_var,
                    'is_duplicate': False
               }
            }
            enemy_data.update(enemy_data_dict)
            ids.append(enemy_object_id)

        def check_radius(self, canvas, shape_var, width_var, height_var):
            shape_color_dict = {
                'Rectangle': 'blueviolet',
                'Triangle': 'darkgreen',
                'Oval': 'orangered',
            }

            chosen_shape = shape_var.get()
            shape_width, shape_height = 0, 0
            try:
                shape_width = int(width_var.get())
                shape_height = int(height_var.get())
            except ValueError:
                print("Wrong Input")
                if chosen_shape == 'Rectangle':
                    shape_width, shape_height = 5, 100
                elif chosen_shape == 'Oval':
                    shape_width, shape_height = 20, 20
                elif chosen_shape == 'Triangle':
                    shape_width, shape_height = 15, 15
            pixel_width = (int)(shape_width / 5) * BLOCK_SIZE
            pixel_height = (int)(shape_height / 5) * BLOCK_SIZE

            if chosen_shape == 'Oval':
                ids.append(canvas.create_oval((canvas_center[0] - (pixel_width)), (canvas_center[1] - (pixel_width)),
                                              (canvas_center[0] + (pixel_width)), (canvas_center[1] + (pixel_width)),
                                              outline=shape_color_dict[chosen_shape], width=4, tags=("circle",)))
            elif chosen_shape == 'Rectangle':
                x0, y0, x2, y2 = (canvas_center[0] - pixel_width), (canvas_center[1] - pixel_height), (
                canvas_center[0]), (canvas_center[1])
                x1, y1, x3, y3 = x2, y0, x0, y2
                xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
                rect_poly = canvas.create_polygon(xy, fill='', outline='blueviolet', width=4, tags=("rectangle",))
                center = [(int)((x2 + x0) / 2), (int)((y2 + y0) / 2)]
                rot_data['id'] = rect_poly
                rot_data['xy'] = xy
                rot_data['center'] = center
            elif chosen_shape == 'Triangle':
                x0, y0, x2, y2 = (canvas_center[0], canvas_center[1], (canvas_center[0] + pixel_width), canvas_center[1])
                x1, y1 = ((int)((x2+x0)/2), canvas_center[1] - pixel_height)
                xy = [(x0, y0), (x1, y1), (x2, y2)]
                tri_poly = canvas.create_polygon(xy, fill = '', outline = 'green', width = 4, tags = ("triangle"))
                center = [x1, (int)((y1 + y0)/2)]
                rot_data['id'] = tri_poly
                rot_data['xy'] = xy
                rot_data['center'] = center

def main():
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    style = ttk.Style(root)
    root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
    root.tk.call('package', 'require', 'awdark')
    style.theme_use('awdark')
    battle_map = tkinter.Canvas(root, bg='white', width=0, height=0, bd=-2, highlightthickness=0)
    battle_map.place(x=0, y=0)
    menu = Menu(root, battle_map)
    menu.place(x=0, y=(int)(3*HEIGHT/4))


    def create_grid(event):
        w = canvas_WIDTH  # Get current width of canvas
        h = canvas_HEIGHT  # Get current height of canvas
        battle_map.delete('grid_line')  # Will only remove the grid_line
        for i in range(0, w, BLOCK_SIZE):
            battle_map.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, BLOCK_SIZE):
            battle_map.create_line([(0, i), (w, i)], tag='grid_line')
    battle_map.bind('<Configure>', create_grid)

    def calculate_newxy_center(objectid):
        coords = battle_map.coords(objectid)
        coord_tuples = []
        tags = battle_map.gettags(objectid)
        new_center = [0, 0]
        for i in range(1, len(coords), 2):
            coord_tuple = (coords[i-1], coords[i])
            coord_tuples.append(coord_tuple)
        if 'triangle' in tags:
            new_center = [(int)(coords[2]), (int)((coords[3] + coords[1]) / 2)]
        else:
            new_center = [(int)((coords[4] + coords[0]) / 2), (int)((coords[5] + coords[1]) / 2)]
        rot_data['xy'] = coord_tuples
        rot_data['center'] = new_center

    def drag_start(event):
        global last_resized
        """Begining drag of an object"""
        # record the item and its location
        drag_data["item"] = battle_map.find_closest(event.x, event.y)[0]
        drag_data_tags = battle_map.gettags(drag_data['item'])
        print(drag_data_tags)
        if 'character' in drag_data_tags or 'rectangle' in drag_data_tags or 'circle' in drag_data_tags or 'triangle' in drag_data_tags:
            battle_map.addtag_withtag("drag",drag_data['item'])
            if drag_data['item'] in hero_data or drag_data['item'] in duplicate_hero_data:
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
        if is_painting:
            closest_object = battle_map.find_closest(event.x, event.y)[0]
            if 'drag' not in battle_map.gettags(closest_object) and 'obstacle' not in battle_map.gettags(
                    closest_object):
                color = 'tan4'
                x1, y1 = (event.x - 1), (event.y - 1)
                x2, y2 = (event.x + 1), (event.y + 1)
                battle_map.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=7, tags=('obstacle',))

    def erase_obstacle(event):
        closest_object = battle_map.find_closest(event.x, event.y)[0]
        if 'obstacle' in battle_map.gettags(closest_object):
            battle_map.delete(closest_object)

    def delete_char(event):
        object_id = battle_map.find_closest(event.x, event.y)[0]
        if 'bg' not in battle_map.gettags(object_id) and 'obstacle' not in battle_map.gettags(object_id) and 'grid_line' not in battle_map.gettags(object_id):
            battle_map.delete(object_id)
            if object_id in hero_data:
                hero_info = hero_data.pop(object_id)
                main_heroes.remove(hero_info['hero_name'])
            elif object_id in duplicate_hero_data:
                duplicate_hero_data.pop(object_id)

    def resize_image(hero_path, char_name, new_width, new_height, x, y):
        temp_dir = "player_models\\temp_resized_sprites\\"
        hero_pic = Image.open(hero_path)
        resized_hero = hero_pic.resize((new_width, new_height), Image.ANTIALIAS)
        resized_hero_path = os.path.join(temp_dir, char_name + "_new_resized.png")
        resized_hero.save(resized_hero_path, "png")
        heroes.append(PhotoImage(file=resized_hero_path))
        battle_map_hero = heroes[-1]
        hero = battle_map.create_image(x, y, image=battle_map_hero, tags=("character", "resizable",))
        ids.append(hero)
        return hero

    def enlarge_shrink(event, enlarge):
        global hero_data, duplicate_hero_data, last_resized
        closest_object = battle_map.find_withtag('resizable')[-1]
        is_dup = False
        data_dict = hero_data
        if closest_object in duplicate_hero_data:
            data_dict = duplicate_hero_data
            is_dup = True
        current_char = data_dict[closest_object]['hero_name']
        hero_path = data_dict[closest_object]['hero_path']
        image_width = data_dict[closest_object]['current_width']
        image_height = data_dict[closest_object]['current_height']

        if enlarge:
            print(f"Making object {closest_object} bigger.")
            new_width = image_width*2
            new_height = image_height*2
        else:
            print(f"Making object {closest_object} smaller.")
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

    def clean_files():
        game_log_path = 'game_log.json'
        try:
            os.remove(game_log_path)
        except FileNotFoundError:
            print('File not found')
        with open(game_log_path, 'w') as f:
            json.dump(hero_data, f)
            json.dump(duplicate_hero_data, f)
            json.dump(enemy_data, f)
        dirs_to_be_cleaned = ["player_models\\base_sprites\\", "player_models\\temp_resized_sprites"]
        for dir in dirs_to_be_cleaned:
            for file in os.listdir(dir):
                file_path = os.path.join(dir, file)
                os.remove(file_path)

    movable_tags = ['character', 'rectangle', 'circle', 'triangle']
    for tag in movable_tags:
        battle_map.tag_bind(tag, "<ButtonPress-1>", drag_start)
        battle_map.tag_bind(tag, "<ButtonRelease-1>", drag_stop)
        battle_map.tag_bind(tag, "<B1-Motion>", drag)

    deletable_tags = movable_tags+['obstacle']
    for tag in deletable_tags:
        battle_map.tag_bind(tag, "<Button-3>", delete_char)

    rotatable_tags = ['rectangle', 'triangle']
    for tag in rotatable_tags:
        battle_map.tag_bind(tag, "<Button-2>", press)
        battle_map.tag_bind(tag, "<B2-Motion>", motion)

    battle_map.bind('<B1-Motion>', lambda event: paint_obstacle(event, movable_tags+rotatable_tags))
    battle_map.bind('<B3-Motion>', erase_obstacle)
    root.bind('<Up>', lambda event: enlarge_shrink(event, True))
    root.bind('<Down>', lambda event: enlarge_shrink(event, False))

    root.mainloop()

    clean_files()



if __name__ == '__main__':
    main()