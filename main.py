#!/usr/bin/env python

import Tkinter as tk
import tkMessageBox
import imtrans
from PIL import Image, ImageTk
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.selected = False
        self._tmp_rect_id = None
        self._zoomVal = tk.IntVar()
        self.grid()
        self.createWidgets()
        

    def createWidgets(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.image = Image.open("kathmandu2.jpg")
        w, h = self.image.size
        photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self, width=w, height=h)
        self.canvas.pack(side='left')
        self.canvas.create_image(w/2,h/2, image=photo)
        self.canvas.image = photo
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)

        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

        self.sidebar = tk.Frame(self)
        self.sidebar.pack(side='right')

        self.zoomRatioLabel = tk.Label(self.sidebar, text='Zoom')
        self.zoomRatioLabel.pack()
        self.zoomSpinbox = tk.Spinbox(self.sidebar)
        self.zoomSpinbox.config( from_=0.2, to=4.0, increment=0.2)
        self.zoomSpinbox.pack()

        self.zoomButton = tk.Button(self.sidebar, text='Zoom', command=self.zoom)
        self.zoomButton.pack()
        self.quitButton = tk.Button(self.sidebar, text='Quit', command=self.quit)
        self.quitButton.pack()

    def zoom(self):
        self._zoomVal = float(self.zoomSpinbox.get())
        if not self.selected:
            tkMessageBox.showwarning(
                "Select a region to zoom", 
                "Please select a region to zoom!")
            return
        # find selected region here
        self.showTransformedImageWindow()

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

        self.canvas.delete(self._tmp_rect_id)

        self._tmp_rect_id = self.canvas.create_rectangle(x0,y0,x1,y1)
        self.selected = True

    def showTransformedImageWindow(self):
        t = tk.Toplevel(self)
        t.wm_title("Zoom: {}".format(self._zoomVal))
        # selected region
        region = self.canvas.coords(self._tmp_rect_id)

        image = imtrans.zoom(self.image, region, self._zoomVal)

        w, h = image.size
        photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(t, width=w, height=h)
        canvas.pack()
        canvas.create_image(w/2,h/2, image=photo)
        canvas.image = photo


app =  Application()
app.master.title('Simple Image Transformer')
app.mainloop()