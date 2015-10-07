#!/usr/bin/env python

import Tkinter as tk
from PIL import Image, ImageTk
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.selected = False
        self._tmp_rect_id = None
        self.grid()
        self.createWidgets()
        

    def createWidgets(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        image = Image.open("kathmandu.jpg")
        w, h = image.size
        photo = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self, width=w, height=h)
        self.canvas.pack()
        self.canvas.create_image(w/2,h/2, image=photo)
        self.canvas.image = photo
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)

        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        #self.quitButton.grid()

    def on_button_press(self, event):
        if self.selected:
            self.canvas.delete(self._tmp_rect_id)
            self.selected = False
            
        self.x = event.x
        self.y = event.y

    def on_mouse_move(self, event):
        x0, y0 = self.x, self.y
        x1, y1 = event.x, event.y
        #if event.x-x1 < 50 and event.y-y1 < 50:
        self.canvas.delete(self._tmp_rect_id)
        self._tmp_rect_id = self.canvas.create_rectangle(x0, y0, x1, y1) #fill="#ccff66")


    def on_button_release(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        self._tmp_rect_id = self.canvas.create_rectangle(x0,y0,x1,y1)
        self.selected = True


app =  Application()
app.master.title('Simple Image Transformer')
app.mainloop()