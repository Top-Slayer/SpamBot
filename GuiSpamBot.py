import tkinter as tk
from tkinter import messagebox
import pyautogui
import win32api
import win32con
import threading
import time

class App:
    x, y = 0, 0
    isRunning = True

    text = str()
    time = int()

    isSpamming = False
    active_get_position = False

    def __init__(self, window):
        window.title("SpamTextBot")
        window.wm_attributes("-topmost", 1)

        # text for input text
        tk.Label(text="Enter your text below here :",width=50).pack()
        # input keyboard
        App.text = tk.Entry(window)
        App.text.pack()

        # text for time of delay
        tk.Label(window,text="Times of delay :").pack()
        # input for time
        App.time = tk.Entry(window,width=10)
        App.time.pack()

        # position of cersor
        tk.Label(window,text="Position of Cursor : ").pack()
        self.position = tk.Label(window, text="{}, {}".format(self.x, self.y))
        self.position.pack()
        tk.Button(window, text="Select position", command=self.changeActiveGetPosition).pack()

        # enter all value to spam
        tk.Label(window, text="\"Ctrl + shift + g\" to start and repeat to stop").pack(pady=10)

        # start and stop title
        self.title_display = tk.Label(window, text="Stop", fg="red")
        self.title_display.pack()

        # exit function
        tk.Label(window, text="\"Ctrl + q\" to exit the program").pack()

        threading.Thread(target=self.threadTasking).start()


    def threadTasking(self):
        self.x = 0
        self.y = 0

        print(f"Application Running [ {App.isRunning} ]")

        while App.isRunning:
            if win32api.GetKeyState(win32con.VK_LBUTTON) < 0 and App.active_get_position: # check if left mouse button is pressed
                self.getPositionClick()
                App.active_get_position = False

            elif win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(ord('Q')) < 0: 
                self.exit_app()

            elif win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(win32con.VK_SHIFT) < 0 and win32api.GetKeyState(ord('G')) < 0:
                # App.isSpamming = True
                threading.Thread(target=self.sendSpambot).start()

            time.sleep(0.1)

        print(f"Application Running [ {App.isRunning} ]")

    def getPositionClick(self):
        App.x, App.y = win32api.GetCursorPos()

        self.x = App.x
        self.y = App.y
        self.position.config(text="{}, {}".format(App.x, App.y))
        print("Position: {}, {}".format(App.x, App.y))

        # if App.x != self.x and App.y != self.y:
        #     self.x = App.x
        #     self.y = App.y
        #     self.position.config(text="{}, {}".format(App.x, App.y))
        #     print("Position: {}, {}".format(App.x, App.y))

    def changeActiveGetPosition(self):
        App.active_get_position = True

    def exit_app(self):
        print("\nExiting application...")
        App.isRunning = False
        window.quit()

    def sendSpambot(self):
        try:
            float(App.time.get()) # get() function use for return text string from entry box
        except ValueError:
            messagebox.showwarning("Warning", "Please enter any number in Time of delay box")
            return

        App.isSpamming = not App.isSpamming
        self.title_display.config(text="Start" if App.isSpamming else "Stop", fg="green" if App.isSpamming else "red")
        print("starting" if App.isSpamming else "stopping")

        while App.isSpamming:
            print('. ', end='')

            pyautogui.moveTo(int(App.x), int(App.y))
            pyautogui.click()
            pyautogui.typewrite(str(App.text.get()))
            time.sleep(float(App.time.get()))
            pyautogui.press('enter')


# main window
window = tk.Tk()
App(window)
window.mainloop()
