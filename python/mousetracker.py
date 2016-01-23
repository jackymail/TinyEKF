#!/usr/bin/env python3

'''
    TinyEKF mouse-tracking example.  

    Inspired by

      http://opencvexamples.blogspot.com/2014/01/kalman-filter-implementation-tracking.html

    Copyright (C) 2016 Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''

DISPLAY_SIZE       = 600
DISPLAY_BORDER     = 4
CANVAS_MARGIN      = 20
DISPLAY_BACKGROUND = 'black'
MOUSE_COLOR        = 'green'
EKF_COLOR          = 'red'
LINE_WIDTH         = 3

import tkinter as tk
import time
from kf import KF

class TrackerFrame(tk.Frame):

    def __init__(self):

        tk.Frame.__init__(self, borderwidth = DISPLAY_BORDER, relief = 'sunken')
        self.master.geometry(str(DISPLAY_SIZE)+ "x" + str(DISPLAY_SIZE))
        self.master.title('TinyEKF Mouse Tracker')
        self.grid()
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.grid(sticky = tk.W+tk.E+tk.N+tk.S)

        canvas_width = DISPLAY_SIZE-2*DISPLAY_BORDER
        canvas_height = DISPLAY_SIZE-2*DISPLAY_BORDER
        
        self.canvas =  tk.Canvas(self, width = canvas_width, height = canvas_height, background = DISPLAY_BACKGROUND)
        self.canvas.grid(row = 0, column = 0)

        self.bind('<Key>', self.handle_key)
        self.canvas.bind('<Motion>', self.handle_motion)

        self.reset_lines()

        self.focus_set()
 
        self.ekf = KF(4, 2)

    def reset_lines(self):

            self.mouse_lines = []
            self.ekf_lines = []

            self.mousex = -1
            self.mousey = -1

    def out_of_bounds(self, coord, dimname):

            return coord < DISPLAY_BORDER or coord > int(self.canvas[dimname])-DISPLAY_BORDER
 
    def handle_motion(self, event):

        mousex, mousey = event.x, event.y

        self.ekf.step((mousex, mousey))

        ekfx, ekfy = int(self.ekf.getX(0)), int(self.ekf.getX(1))

        if self.mousex != -1:
            if self.out_of_bounds(mousex, 'width') or self.out_of_bounds(mousey, 'height'):
                [self.canvas.delete(line) for line in self.mouse_lines]
                [self.canvas.delete(line) for line in self.ekf_lines]
                self.reset_lines()
            else:
                self.mouse_lines.append(self.canvas.create_line(self.mousex, self.mousey, mousex, mousey, 
                    fill=MOUSE_COLOR, width=LINE_WIDTH))
                self.ekf_lines.append(self.canvas.create_line(self.ekfx, self.ekfy, ekfx, ekfy, 
                    fill=EKF_COLOR, width=LINE_WIDTH))


        self.mousex = mousex
        self.mousey = mousey

        self.ekfx = ekfx
        self.ekfy = ekfy

        time.sleep(.1)
                
    def handle_key(self, event):

        # Make sure the frame is receiving input!
        self.focus_force()
        if event.keysym == 'Escape':
            exit(0)

if __name__ == '__main__':
    
    TrackerFrame().mainloop()




