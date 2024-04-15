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
        App.time = tk.Entry(window,width=3)
        App.time.pack()

        # position of cersor
        tk.Label(window,text="Position of Cursor : ").pack()
        self.position = tk.Label(window, text="{}, {}".format(self.x, self.y))
        self.position.pack()

        # enter all value to spam
        tk.Label(window, text="\"Ctrl + shift + g\" to start and repeat to stop").pack(pady=10)

        # exit function
        tk.Label(window, text="\"Ctrl + q\" to exit the program").pack()

        threading.Thread(target=self.threadTasking).start()


    def threadTasking(self):
        self.x = 0
        self.y = 0

        print(f"Application Running [ {App.isRunning} ]")

        while App.isRunning:
            if win32api.GetKeyState(win32con.VK_LBUTTON) < 0: # check if left mouse button is pressed
                self.getPositionClick()

            elif win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(ord('Q')) < 0: 
                # self.exit_app()
                threading.Thread(target=self.exit_app).start()

            elif win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(win32con.VK_SHIFT) < 0 and win32api.GetKeyState(ord('G')) < 0:
                # App.isSpamming = True
                time.sleep(1)
                threading.Thread(target=self.sendSpambot).start()

        print(f"Application Running [ {App.isRunning} ]")

    def getPositionClick(self):
        App.x, App.y = win32api.GetCursorPos()

        if App.x != self.x and App.y != self.y:
            self.x = App.x
            self.y = App.y
            self.position.config(text="{}, {}".format(App.x, App.y))
            print("[Func: getPositionClick] Position: {}, {}".format(App.x, App.y))

    def exit_app(self):
        print("\nExiting application...\n")
        App.isRunning = False
        window.quit()

    def sendSpambot(self):
        App.isSpamming = not App.isSpamming
        print("starting" if App.isSpamming else "stopping")

        try:
            float(App.time.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter any number in Time of delay box")
            return

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
