# canvas_WIDTH, canvas_HEIGHT = (int)(WIDTH/1.215), HEIGHT

# class Spawner(Frame):
#     def __init__(self, master, canvas):
#         super().__init__(master)
#         frame_width, frame_height = (WIDTH-canvas_WIDTH), HEIGHT/3
#         #frame_width, frame_height = WIDTH, (int)(HEIGHT/4)
#         self.config(bg=background_color,width=frame_width, height=frame_height)
#         self.pack_propagate(False)
#         self.grid_propagate(False)
#         self.columnconfigure((0,1), weight=1)
#
#         players = ['Swig', 'Hardin', 'Silene', 'Bones']
#         hero_var = StringVar(self)
#         hero_var.set(players[0])
#         self.hero_chooser = ttk.OptionMenu(self, hero_var, *players)
#         self.hero_chooser.grid(row=0, column=0, sticky='EW')
#
#         self.hero_spawner = ttk.Button(self, text='Spawn Hero', command=lambda:self.spawn_hero(canvas, hero_var))
#         self.hero_spawner.grid(row=0, column=1, sticky='EW')
#
#         size_options = list(SIZES.keys())
#         size_var = StringVar(self)
#         size_var.set(size_options[2])
#         self.enemy_size_choice = ttk.OptionMenu(self, size_var, *size_options)
#         self.enemy_size_choice.grid(row=1, column=0, sticky='EW')
#
#         self.enemy_spawner = ttk.Button(self, text='Spawn Enemy', command=lambda: self.spawn_enemy(canvas, size_var.get()))
#         self.enemy_spawner.grid(row=1, column=1, sticky='EW')
#
#         width_var = StringVar(self)
#         height_var = StringVar(self)
#         self.width_label = ttk.Label(self, text='Spell width/radius (ft)')
#         self.width_label.grid(row=2, column=0, sticky='EW',ipadx = 5)
#         self.entry_width = ttk.Entry(self, textvariable=width_var)
#         self.entry_width.grid(row=2, column=1, sticky='EW')
#         self.height_label = ttk.Label(self, text='Spell height/radius (ft)')
#         self.height_label.grid(row=3, column=0, sticky='EW', ipadx = 5)
#         self.entry_height = ttk.Entry(self, textvariable=height_var)
#         self.entry_height.grid(row=3, column=1, sticky='EW')
#
#         shapes = ['Rectangle', 'Triangle', 'Oval']
#         shape_var = StringVar(self)
#         shape_var.set(shapes[0])
#         self.shape_chooser = ttk.OptionMenu(self, shape_var, *shapes)
#         self.shape_chooser.grid(row=4, column=0, sticky='EW')
#
#         self.sphere_checker = ttk.Button(self, text='Check Radius', command=lambda: self.check_radius(canvas, shape_var, width_var, height_var))
#         self.sphere_checker.grid(row=4, column=1, sticky='EW')
#
#         paint_var = BooleanVar()
#         paint_var.set(False)
#         self.paint_button_1 = ttk.Radiobutton(self, text='Pen Up', variable=paint_var, value=False, command = lambda: self.is_painting(paint_var.get()))
#         self.paint_button_1.grid(row=5, column=0, sticky='EW')
#         self.paint_button_2 = ttk.Radiobutton(self, text='Pen Down', variable=paint_var, value=True, command = lambda: self.is_painting(paint_var.get()))
#         self.paint_button_2.grid(row=5, column=1, sticky='EW')
#
#
#
#     def is_painting(self, value):
#         global is_painting
#         is_painting = value
#
#     def spawn_hero(self, canvas, hero_var):
#         original_hero_image_dir = "player_models\\original\\"
#         base_hero_sprites_dir = "player_models\\base_sprites\\"
#         chosen_hero = hero_var.get()
#         base_sprite_file = chosen_hero + "_resized.png"
#         base_sprite_path = base_hero_sprites_dir + base_sprite_file
#         original_image_path = os.path.join(original_hero_image_dir, (chosen_hero + "_original.png"))
#         if base_sprite_file not in os.listdir(base_hero_sprites_dir):
#             original_image_path = os.path.join(original_hero_image_dir,(chosen_hero + "_original.png"))
#             image = Image.open(original_image_path)
#             base_sprite = image.resize((HERO_WIDTH, HERO_HEIGHT), Image.ANTIALIAS)
#             base_sprite.save(base_sprite_path, "png")
#         if chosen_hero in main_heroes:
#             image = Image.open(base_sprite_path)
#             d = ImageDraw.Draw(image)
#             d.rectangle([(0,5),(HERO_WIDTH,HERO_HEIGHT)], width=2)
#             dup_hero_image_path = os.path.join(base_hero_sprites_dir, (chosen_hero + '_duplicate_resized.png'))
#             image.save(dup_hero_image_path, "png")
#             heroes.append(PhotoImage(file=dup_hero_image_path))
#         else:
#             heroes.append(PhotoImage(file=base_sprite_path))
#         canvas.battle_map_hero = heroes[-1]
#         hero_object_id = canvas.create_image(canvas_center[0], canvas_center[1], image=heroes[-1], tags=("character",))
#         data_dict = {hero_object_id :
#             {
#                 'hero_name': chosen_hero,
#                 'hero_path': original_image_path,
#                 'base_width': HERO_WIDTH,
#                 'base_height': HERO_HEIGHT,
#                 'current_width': HERO_WIDTH,
#                 'current_height': HERO_HEIGHT
#             }
#         }
#         ids.append(hero_object_id)
#         if chosen_hero not in main_heroes:
#             main_heroes.append(chosen_hero)
#             hero_data.update(data_dict)
#         else:
#             duplicate_hero_data.update(data_dict)
#
#         # print(hero_data)
#         # print(duplicate_hero_data)
#
#     def spawn_enemy(self, canvas, size_var):
#         ids.append(canvas.create_oval(canvas_center[0], canvas_center[1], canvas_center[0]+(45*SIZES[size_var]), canvas_center[1]+(45*SIZES[size_var]), outline='black', fill='red', tags=("character",)))
#
#     def check_radius(self, canvas, shape_var, width_var, height_var):
#         shape_color_dict = {
#             'Rectangle': 'blueviolet',
#             'Triangle': 'darkgreen',
#             'Oval': 'orangered',
#         }
#
#         chosen_shape = shape_var.get()
#         shape_width, shape_height = 0,0
#         try:
#             shape_width = int(width_var.get())
#             shape_height = int(height_var.get())
#         except ValueError:
#             print("Wrong Input")
#             if chosen_shape == 'Rectangle':
#                 shape_width, shape_height = 5, 100
#             elif chosen_shape == 'Oval':
#                 shape_width, shape_height = 20, 20
#         pixel_width = (int)(shape_width/5)*BLOCK_SIZE
#         pixel_height = (int)(shape_height/5)*BLOCK_SIZE
#
#         if chosen_shape == 'Oval':
#             ids.append(canvas.create_oval((canvas_center[0] - (pixel_width)), (canvas_center[1] - (pixel_width)), (canvas_center[0] + (pixel_width)), (canvas_center[1] + (pixel_width)), outline=shape_color_dict[chosen_shape], width=4, tags=("circle",)))
#         elif chosen_shape == 'Rectangle':
#             x0, y0, x2, y2 = (canvas_center[0]-pixel_width), (canvas_center[1]-pixel_height), (canvas_center[0]), (canvas_center[1])
#             x1, y1, x3, y3 = x2, y0, x0, y2
#             xy = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
#             rect_poly = canvas.create_polygon(xy, fill='', outline='blueviolet', width=4, tags=("rectangle",))
#             center = [(int)((x2 + x0)/2), (int)((y2 + y0)/2)]
#             rot_data['id'] = rect_poly
#             rot_data['xy'] = xy
#             rot_data['center'] = center
#
# class Initializer(Frame):
#     def __init__ (self, master, canvas):
#         super().__init__(master)
#         frame_width, frame_height = (WIDTH - canvas_WIDTH), HEIGHT / 3
#         #frame_width, frame_height = WIDTH, (int)(HEIGHT/4)
#         self.config(bg=background_color, width=frame_width, height=frame_height)
#         self.pack_propagate(False)
#         self.grid_propagate(False)
#         self.columnconfigure((0, 1), weight=1)
#
#         self.battlemap_bg_label = ttk.Label(self, text='Find a picture to use for the battlemap:')
#         self.battlemap_bg_label.grid(row = 0, columnspan = 2, sticky = 'EW')
#         self.battlemap_bg_button = ttk.Button(self, text='Browse', command = lambda: choose_bm_bg(self, canvas))
#         self.battlemap_bg_button.grid(row = 1, columnspan = 2, sticky = 'EW')
#
#
#         def choose_bm_bg(self, canvas):
#             global battlemap_bg
#             try:
#                 filename = askopenfilename(filetypes=[('Image Files', ['*.jpeg', "*.jpg", "*.png", "*.img"])])
#                 if filename is not None:
#                     image = Image.open(filename)
#                     resized = image.resize((canvas_WIDTH, canvas_HEIGHT), Image.ANTIALIAS)
#                     resized.save('battlemap_bg.png', "png")
#                     battlemap_bg = PhotoImage(file='battlemap_bg.png')
#                     canvas.create_image(0, 0, image = battlemap_bg, anchor = 'nw')
#                     canvas.config(width=canvas_WIDTH, height = HEIGHT)
#                     canvas.update()
#             except AttributeError:
#                 print("No image input")
#                 self.master.destroy()
#
# class Status(Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         frame_width, frame_height = (WIDTH - canvas_WIDTH), HEIGHT / 3
#         #frame_width, frame_height = WIDTH, (int)(HEIGHT/4)
#         self.config(bg=background_color, width=frame_width, height=frame_height)
#         self.pack_propagate(False)
#         self.grid_propagate(False)
#         self.columnconfigure((0, 1), weight=1)
# def shrink(event):
#     global hero_data, duplicate_hero_data, last_resized
#     closest_object = battle_map.find_withtag('resizable')[-1]
#     print(f"Making object {closest_object} bigger.")
#     current_char = ''
#     image_width = 0
#     image_height = 0
#     hero_path = ''
#     is_dup = False
#     data_dict = hero_data
#     if closest_object in duplicate_hero_data:
#         data_dict = duplicate_hero_data
#         is_dup = True
#     current_char = data_dict[closest_object]['hero_name']
#     hero_path = data_dict[closest_object]['hero_path']
#     image_width = data_dict[closest_object]['current_width']
#     image_height = data_dict[closest_object]['current_height']
#
#     new_width = (int)(image_width / 2)
#     new_height = (int)(image_height / 2)
#
#     if closest_object in ids:
#         battle_map.delete(closest_object)
#         ids.remove(closest_object)
#         new_hero_object_id = resize_image(hero_path, current_char, new_width, new_height, event.x, event.y, is_dup)
#         data_dict[new_hero_object_id] = data_dict.pop(closest_object)
#         data_dict[new_hero_object_id]['current_width'] = new_width
#         data_dict[new_hero_object_id]['current_height'] = new_height
#         if is_dup:
#             duplicate_hero_data = data_dict
#         else:
#             hero_data = data_dict
#         last_resized = new_hero_object_id