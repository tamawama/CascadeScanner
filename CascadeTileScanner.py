import os
import time
import tkinter as tk
import threading
import win32con
import win32api
import pywintypes

# set to true if you're an alt tab gamer
loadedMessage = False

tilesets = {
    "IntHydroponics.level": "Dogshit (3)",
    "IntLivingQuarters.level": "Ramp (3)",
    "IntCargoBay.level": "Cargo Bay (3)",
    "IntAmphitheatre.level": "Amphitheatre (3)",
    "IntIndoctrinationHall.level": "Hall (3)",
    "IntLunaroCourt.level": "Lunaro (3)",
    "IntCellBlockA.level": "Brig (3)",
    "IntSchool.level": "Schoolyard (4)",
    "IntPark.level": "Statue (4)",
    "IntParkB.level": "Park (4)",
    "IntParkC.level": "Roost (4)",
    "IntShuttleBay.level": "Shipyard (5)"
}


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


class Overlay:
    def __init__(self):
        pass

    def run(self):
        threading.Thread(target=self.track_tiles).start()

    def track_tiles(self):
        path = os.getenv('LOCALAPPDATA') + r'\Warframe\EE.log'
        logfile = open(path)
        loglines = follow(logfile)
        searching = False
        for line in loglines:
            if not line:
                continue
            if "/Lotus/Levels/Proc/Zariman/ZarimanDirectionalSurvival generating layout" in line:
                searching = True
            elif searching:
                print(line)
            if searching and "ResourceLoader" in line:
                searching = False

if __name__ == '__main__':
    print("Cascade Tile Searcher Started; Close this window when done using.")
    overlay = Overlay()
    overlay.run()
