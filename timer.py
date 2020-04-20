#!/usr/bin/env python
# coding: utf-8

# The goal of this little project is to create a Windows 10 App to implement a "Pomodoro-Technique" style timer.
# I'll use TkInter.

# pip install pyinstaller

import tkinter as tk
import datetime
import winsound

class Crono(object):
    def __init__(self, master, start_time):
        self.master = master
        master.title("Pomodoro")
        self.start_time = start_time
        self.current_time = datetime.datetime.now()
        self.delta = datetime.timedelta(0)
        self.result = datetime.timedelta(0)
        self.running = False
        self.paused = False
        self.acumulated = datetime.timedelta(0)

        # Frame for the labels
        self.frame_1 = tk.Frame(master) # width=... optional
        self.frame_1.pack()
        # self.frame.pack_propagate(0)
        
        # Frame for the buttons
        self.frame_2 = tk.Frame(master)
        self.frame_2.pack()

        
        # Frame for the sliders
        self.frame_3 = tk.Frame(master)
        self.frame_3.pack()
        
        # Frame for modes
        self.frame_4 = tk.Frame(master)
        self.frame_4.pack()
        
        self.delta_seconds = self.delta.total_seconds()
        self.hours = tk.Label(self.frame_1, font=("Courier New",30))
        self.minutes = tk.Label(self.frame_1, font=("Courier New",30))
        self.seconds = tk.Label(self.frame_1, font=("Courier New",30))
        self.u_seconds = tk.Label(self.frame_1, font=("Courier New",30))
        self.w_labels()
        self.hours.pack(side=tk.LEFT)
        self.minutes.pack(side=tk.LEFT)
        self.seconds.pack(side=tk.LEFT)
        self.u_seconds.pack(side=tk.LEFT)
        
        # Start, Pause buttons
        self.bt_start = tk.Button(self.frame_2, text="Start", width=10, command=self.start)
        self.bt_start.pack(side=tk.LEFT)
        self.bt_pause = tk.Button(self.frame_2, text="Pause", width=10, command=self.pause)
        self.bt_pause.pack(side=tk.LEFT)

        # sliders
        self.w1 = tk.Scale(self.frame_3, from_=0, to=23, orient=tk.VERTICAL, showvalue=0, command=self.read_sliders)
        self.w1.set(0)
        self.w2 = tk.Scale(self.frame_3, from_=0, to=59, orient=tk.VERTICAL, showvalue=0, command=self.read_sliders)
        self.w2.set(0)
        self.w3 = tk.Scale(self.frame_3, from_=0, to=59, orient=tk.VERTICAL, showvalue=0, command=self.read_sliders)
        self.w3.set(0)
        self.w1.pack(side=tk.LEFT)
        self.w2.pack(side=tk.LEFT)
        self.w3.pack(side=tk.LEFT)
        
        # Mode buttons
        self.bt_stopwatch = tk.Button(self.frame_4, text="Stopwatch", width=10, command=self.stopwatch, relief=tk.SUNKEN)
        self.bt_stopwatch.pack(side=tk.LEFT)
        self.bt_timer = tk.Button(self.frame_4, text="Timer", width=10, command=self.timer)
        self.bt_timer.pack(side=tk.RIGHT)

        self.timer()
            
    def refresh(self):
        if self.running == True:
            self.current_time = datetime.datetime.now()
            if self.mode == "Stopwatch":
                self.result = (self.current_time - self.start_time + self.acumulated)
                self.w_labels()
            elif self.mode == "Timer":
                self.result = self.result - (self.current_time - self.start_time + self.acumulated)
                self.start_time = self.current_time
                if self.result <= datetime.timedelta(0):
                    self.goal_reached()
                self.w_labels()
            self.master.after(10, self.refresh)
        else:
            self.master.after_cancel

    def start(self):
        if self.running == False:
            if self.paused == False:
                self.start_time = datetime.datetime.now()
                self.paused_time = self.start_time
                self.acumulated = datetime.timedelta(0)
                self.running = True
                self.bt_pause.configure(text="Pause")
                self.bt_start.configure(text="Stop")
                self.refresh()
            elif self.paused == True:
                self.running = False
                self.paused = False
                self.result = datetime.timedelta(0)
                self.w_labels()
                self.bt_start.configure(text="Start")
                self.bt_pause.configure(text="Pause")
        elif self.running == True:
            self.running = False
            self.result = datetime.timedelta(0)
            self.w_labels()
            self.bt_start.configure(text="Start")

    def pause(self):
        if self.running == True:
            self.running = False
            self.paused = True
            self.acumulated = self.result
            self.bt_pause.configure(text="Resume")
        elif self.running == False:
            if self.paused == True:
                self.running = True
                self.paused = False
                self.start_time = datetime.datetime.now()
                self.refresh()
                self.bt_pause.configure(text="Pause")
            elif self.paused == False:
                pass
    
    def w_labels(self):
        self.delta_ts = self.result.total_seconds()
        self.delta_h = int(self.delta_ts) // 3600
        self.delta_m = int(self.delta_ts % 3600) // 60
        self.delta_s = int(self.delta_ts) % 60
        self.delta_us = self.result.microseconds
        self.hours.configure(text=str(self.delta_h).zfill(2)+":")
        self.minutes.configure(text=str(self.delta_m).zfill(2)+":")
        self.seconds.configure(text=str(self.delta_s).zfill(2)+".")
        self.u_seconds.configure(text=str(self.delta_us).zfill(3)[0:3])

    def timer(self):
        self.running = False
        self.paused = False
        self.mode = "Timer"
        self.bt_pause.configure(text="Pause")
        self.bt_start.configure(text="Start")
        self.read_sliders(0)
        self.w_labels()
        self.w1.pack(side=tk.LEFT)
        self.w2.pack(side=tk.LEFT)
        self.w3.pack(side=tk.LEFT)        
        self.bt_timer.config(relief=tk.SUNKEN)
        self.bt_stopwatch.config(relief=tk.RAISED)
        
    def stopwatch(self):
        self.w1.pack_forget()
        self.w2.pack_forget()
        self.w3.pack_forget()
        self.running = False
        self.result=datetime.timedelta(0)
        self.bt_pause.configure(text="Pause")
        self.bt_start.configure(text="Start")
        self.bt_stopwatch.config(relief=tk.SUNKEN)
        self.bt_timer.config(relief=tk.RAISED)
        self.mode = "Stopwatch"
        self.w_labels()
        

    def read_sliders(self, val):
        self.result=datetime.timedelta(hours=self.w1.get(), minutes=self.w2.get(), seconds=self.w3.get())
        self.w_labels()
    
    def goal_reached(self):
        self.running = False
        self.paused = False
        self.result = datetime.timedelta(0)
        self.bt_start.configure(text="Start")
        self.w_labels()
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

        
if __name__=='__main__':
    root = tk.Tk()
    app = Crono(root, datetime.datetime.now())
    root.iconbitmap("favicon.ico")
    root.mainloop()

# pyinstaller.exe --onefile --icon=favicon.ico --noconsole timer.py 