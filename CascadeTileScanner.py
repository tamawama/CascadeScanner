#!/usr/bin/env python
# Someone else get it to work perfectly I cba - Abu-Al-Gaming

import os
import time
import gi
import threading
import cairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk

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

class Overlay(Gtk.Window):
    def __init__(self):
        super().__init__(title="Balls Overlay")

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_app_paintable(True)
        self.set_default_size(200, 50)
        self.move(0, 0)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and self.get_screen().is_composited():
            self.set_visual(visual)

        self.connect("draw", self.on_draw)

        self.label = Gtk.Label(label="Waiting for Data...")
        self.label.set_name("overlay_label")

        css = b"""
        #overlay_label {
            font-size: 15px;
            color: white;
        }
        """
        self.apply_css(css)

        self.add(self.label)
        self.show_all()

    def apply_css(self, css_data):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0.6)
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.paint()

    def update_overlay(self, text, text_color):
        self.label.set_text(text)
        if text_color == "red":
            self.apply_css(b"#overlay_label { color: red; }")
        elif text_color == "green":
            self.apply_css(b"#overlay_label { color: green; }")
        elif text_color == "cyan":
            self.apply_css(b"#overlay_label { color: cyan; }")
        elif text_color == "magenta":
            self.apply_css(b"#overlay_label { color: magenta; }")

    def run(self):
        threading.Thread(target=self.track_tiles).start()
        self.update_overlay("Awaiting Cascade...", "red")
        Gtk.main()

    def track_tiles(self):
        global loadedMessage, tilesets
        path = os.path.expanduser('~') + '/.local/share/Steam/steamapps/compatdata/230410/pfx/drive_c/users/steamuser/AppData/Local/Warframe/EE.log'
        logfile = open(path, encoding="utf8", errors="ignore")
        loglines = follow(logfile)
        searching = False
        tiles = ""
        exocount = 0
        tilecount = 0
        for line in loglines:
            if not line:
                continue

            # Reset when the Layer255 is found
            if loadedMessage:
                if "Play()" in line and "Layer255" in line and not "LotusCinematic" in line:
                    self.update_tiles_overlay(exocount, tiles)
                    tiles = ""
                    exocount = 0

            # Start searching for tiles
            if "/Lotus/Levels/Proc/Zariman/ZarimanDirectionalSurvival generating layout" in line:
                searching = True

            # Reset if mission has ended or ship loaded
            if not searching and ("/Lotus/Levels/Proc/TheNewWar/PartTwo/TNWDrifterCampMain" in line or "/Lotus/Levels/Proc/PlayerShip" in line):
                self.update_overlay("Awaiting Cascade...", "red")

            # Detect the spawned tiles
            if "Added streaming layer /Lotus/Levels/Zariman/" in line:
                for key in list(tilesets.keys()):
                    if key in line:
                        tilecount += 1
                        if tilecount < 3:
                            tiles += tilesets.get(key) + " -> "
                        elif tilecount == 3:
                            tiles += tilesets.get(key)

                        exocount += int(tilesets.get(key).split("(")[1][0])
                        del tilesets[key]
                        break

            # Finalize tile detection and update overlay
            elif searching and "ResourceLoader" in line:
                self.update_tiles_overlay(exocount, tiles)
                searching = False
                tilecount = 0
                if not loadedMessage:
                    tiles = ""
                    exocount = 0
                tilesets = original_tilesets.copy()  # Reset tilesets after 3 tiles found

    def update_tiles_overlay(self, exocount, tiles):
        """Updates the overlay based on the number of exocount."""
        if exocount <= 10:
            self.update_overlay(tiles, "red")
        elif exocount == 11:
            self.update_overlay(tiles, "green")
        elif exocount == 12:
            self.update_overlay(tiles, "cyan")
        elif exocount == 13:
            self.update_overlay(tiles, "magenta")


if __name__ == '__main__':
    overlay = Overlay()
    overlay.run()
