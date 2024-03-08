import os
import time
import threading


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
        self.track_tiles()

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
            elif searching and ("I:" in line or "C:" in line):
                print(line)
            if searching and "ResourceLoader" in line:
                searching = False
                print()

if __name__ == '__main__':
    print("Cascade Tile Searcher Started; Close this window when done using.")
    overlay = Overlay()
    overlay.run()
