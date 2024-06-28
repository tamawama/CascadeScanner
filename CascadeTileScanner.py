import os
import time
import tkinter as tk
import threading
import win32con
import win32api
import pywintypes

# set to true if you're an alt tab gamer
loadedMessage = True

connectors = {
    "test": "bwah"
}

original_tilesets = {
    "IntHydroponics": "Dogshit (3)",
    "IntLivingQuarters": "Ramp (3)",
    "IntCargoBay": "Cargo Bay (3)",
    "IntAmphitheatre": "Amphitheatre (3)",
    "IntIndoctrinationHall": "Hall (3)",
    "IntLunaroCourt": "Lunaro (3)",
    "IntCellBlockA": "Brig (3)",
    "IntSchool": "Schoolyard (4)",
    "IntPark": "Statue (4)",
    "IntParkB": "Park (4)",
    "IntParkC": "Roost (4)",
    "IntShuttleBay": "Shipyard (5)"
}

tilesets = original_tilesets.copy()

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
        self.path = None
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("10x10")
        self.root.configure(bg='black')
        self.root.attributes("-alpha", 0.5)
        self.enable_overlay = True
        self.label = tk.Label(self.root, text="i stole this from wally :D",
                              fg="white", bg="black", font=('Times New Roman', 15, ''))
        self.label.pack(fill="both", expand=True)

    def update_overlay(self, text, text_color):
        self.label.config(text=text, fg=text_color)
        self.root.update_idletasks()
        width = self.label.winfo_reqwidth() + 2  # Add some padding
        self.root.geometry(f"{width}x40")

        hWindow = pywintypes.HANDLE(int(self.label.master.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    def run(self):
        threading.Thread(target=self.track_tiles).start()
        self.update_overlay("Awaiting Cascade...", "red")
        self.root.mainloop()

    def track_tiles(self):
        global loadedMessage, tilesets
        path = os.getenv('LOCALAPPDATA') + r'\Warframe\EE.log'
        logfile = open(path, encoding="utf8", errors="ignore")
        loglines = follow(logfile)
        searching = False
        tiles = ""
        exocount = 0
        tilecount = 0
        for line in loglines:
            # if null skip to next line
            if not line:
                continue

            if loadedMessage:
                if "Play()" in line and "Layer255" in line and not "LotusCinematic" in line:
                    if exocount <= 10:
                        self.update_overlay(tiles, "red")
                    elif exocount == 11:
                        self.update_overlay(tiles, "green")
                    elif exocount == 12:
                        self.update_overlay(tiles, "cyan")
                    elif exocount == 13:
                        self.update_overlay(tiles, "magenta")
                    tiles = ""
                    exocount = 0

            if "/Lotus/Levels/Proc/Zariman/ZarimanDirectionalSurvival generating layout" in line:
                searching = True
            if not searching and ("/Lotus/Levels/Proc/TheNewWar/PartTwo/TNWDrifterCampMain" in line or "/Lotus/Levels/Proc/PlayerShip" in line):
                self.update_overlay("Awaiting Cascade...", "red")
            if "Added streaming layer /Lotus/Levels/Zariman/" in line:
                for key in list(tilesets.keys()):
                    if key in line:
                        print(line, key)
                        tilecount += 1
                        if tilecount < 3:
                            tiles = tiles + tilesets.get(key) + " -> "
                        if tilecount == 3:
                            tiles = tiles + tilesets.get(key)
                        exocount += int(tilesets.get(key).split("(")[1][0])
                        del tilesets[key]  # Remove the found tile
                        break
            elif searching and "ResourceLoader" in line:
                if exocount <= 10:
                    self.update_overlay(tiles, "red")
                elif exocount == 11:
                    self.update_overlay(tiles, "green")
                elif exocount == 12:
                    self.update_overlay(tiles, "cyan")
                elif exocount == 13:
                    self.update_overlay(tiles, "magenta")
                searching = False
                tilecount = 0
                if not loadedMessage:
                    tiles = ""
                    exocount = 0
                tilesets = original_tilesets.copy()  # Reset the tilesets after 3 tiles found

if __name__ == '__main__':
    overlay = Overlay()
    overlay.run()
