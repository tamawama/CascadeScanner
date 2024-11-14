import os
import time
import tkinter as tk
import threading
import win32con
import win32api
import pywintypes
from datetime import datetime

# Set to True if you're an alt-tab gamer
loadedMessage = True

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
        global loadedMessage
        path = os.getenv('LOCALAPPDATA') + r'\Warframe\EE.log'
        
        # Check if log file exists
        if not os.path.isfile(path):
            print("Log file not found.")
            return
        
        color_map = {10: "red", 11: "green", 12: "cyan", 13: "magenta"}  

        with open(path, encoding="utf8", errors="ignore") as logfile:
            loglines = follow(logfile)
            searching = False
            exocount = 0
            attempts = 0
            
            for line in loglines:
                now = datetime.now()
                milliseconds = now.microsecond // 1000
                timestamp = now.strftime(f'%H:%M:%S.{milliseconds:03d}')
                
                if loadedMessage and "Play()" in line and "Layer255" in line and not "LotusCinematic" in line:
                    color = color_map.get(exocount, "red")
                    self.update_overlay(f"Exo Count: {exocount}", color)
                    exocount = 0

                if "/Lotus/Levels/Proc/Zariman/ZarimanDirectionalSurvival generating layout" in line:
                    searching = True
                    exocount = 0
                    attempts += 1
                    print(f"[Attempt {attempts}]")

                if not searching and ("/Lotus/Levels/Proc/TheNewWar/PartTwo/TNWDrifterCampMain" in line or
                                      "/Lotus/Levels/Proc/PlayerShip" in line):
                    self.update_overlay("Awaiting Cascade...", "red")

                if "ZarimanSurvivalMission.lua: ID" in line:
                    exocount = int(line.split('=')[-1].strip())
                    print(f"[{timestamp}] - {line}")
                    
                elif searching and "ReplicaInit complete" in line:
                    color = color_map.get(exocount, "red")
                    self.update_overlay(f"Exo Count: {exocount}", color)
                    searching = False
                    
                    if not loadedMessage:
                        exocount = 0

if __name__ == '__main__':
    overlay = Overlay()
    overlay.run()