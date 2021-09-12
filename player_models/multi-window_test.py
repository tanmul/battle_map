import tkinter as tk

window_layers = []

class Demo1:
    def __init__(self, master):
        self.master = master
        self.master.geometry('500x500')
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        window_layers.append(self.newWindow)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.master.destroy()
        self.master.geometry('1280x700')
        self.canvas = tk.Canvas(self.master, bg = 'white', width = 1280, height =720)
        self.quitButton = tk.Button(self.canvas, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.canvas.pack()

    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()