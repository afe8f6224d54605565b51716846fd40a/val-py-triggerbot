import json
import sys
import time
from ctypes import WinDLL

import keyboard
import numpy as np
import win32api
from mss import mss as mss_module

# Constants
RGB_COLOR = (250, 100, 250) # RGB color of the enemy


def exiting():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()
        except:
            raise SystemExit


user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

ZONE = 5
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE),
    int(HEIGHT / 2 - ZONE),
    int(WIDTH / 2 + ZONE),
    int(HEIGHT / 2 + ZONE),
)


class TriggerBot:
    def __init__(self):
        self.sct = mss_module()
        self.triggerbot = False
        self.exit_program = False

        with open('config.json') as json_file:
            data = json.load(json_file)

        try:
            self.trigger_hotkey = int(data["trigger_hotkey"], 16)
            self.trigger_delay = data["trigger_delay"]
            self.base_delay = data["base_delay"]
            self.color_tolerance = data["color_tolerance"]
            self.key_bind = data["key_bind"]
            self.R, self.G, self.B = RGB_COLOR
        except:
            exiting()

    def searcherweeso(self):
        img = np.array(self.sct.grab(GRAB_ZONE))

        color_mask = (
            (img[:, :, 0] > self.R - self.color_tolerance) & (img[:, :, 0] < self.R + self.color_tolerance) &
            (img[:, :, 1] > self.G - self.color_tolerance) & (img[:, :, 1] < self.G + self.color_tolerance) &
            (img[:, :, 2] > self.B - self.color_tolerance) & (img[:, :, 2] < self.B + self.color_tolerance)
    )

        if self.triggerbot and np.any(color_mask):
            delay_percentage = self.trigger_delay / 100.0
            actual_delay = self.base_delay + self.base_delay * delay_percentage
            time.sleep(actual_delay)
            keyboard.press_and_release(self.key_bind)

    def hold(self):
        while True:
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True
                self.searcherweeso()
            else:
                time.sleep(0.1)
            if keyboard.is_pressed("ctrl+shift+x"):  # ctrl+shift+x to exit
                self.exit_program = True
                exiting()

    def starterweeso(self):
        while not self.exit_program:
            self.hold()

TriggerBot().starterweeso()