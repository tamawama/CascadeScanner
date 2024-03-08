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
        self.path = None
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("10x10")
        self.root.configure(bg='black')
        self.root.attributes("-alpha", 0.5)
        self.enable_overlay = True
        self.label = tk.Label(self.root, text="i stole this from wally :D", fg="white", bg="black",
                              font=('Times New Roman', 15, ''))
        self.label.pack(fill="both", expand=True)

        self.offset_x = 0
        self.offset_y = 0

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
        path = os.getenv('LOCALAPPDATA') + r'\Warframe\EE.log'
        logfile = open(path)
        loglines = follow(logfile)
        searching = False
        tiles = ""
        exocount = 0
        for line in loglines:
            if not line:
                continue
            global loadedMessage
            if loadedMessage:
                if "Cinematic /LotusCinematic0 Play()" in line:
                    self.update_overlay("Awaiting Cascade...  [LOADED]", "red")
                if "Play()" in line and "Layer255" in line and not "LotusCinematic" in line:
                    tiles = tiles + "  [LOADED]"
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
            if searching and "I:" in line:
                if tiles:
                    tiles = tiles + " -> "
                for key in tilesets.keys():
                    if key in line:
                        tiles = tiles + tilesets.get(key)
                        exocount += int(tilesets.get(key).split("(")[1][0])
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
                if not loadedMessage:
                    tiles = ""
                    exocount = 0


if __name__ == '__main__':
    print("Cascade Tile Searcher Started; Close this window when done using.")
    overlay = Overlay()
    overlay.run()
