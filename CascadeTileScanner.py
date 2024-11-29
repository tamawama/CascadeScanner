import os
import time
import tkinter as tk
import threading
import win32con
import win32api
import pywintypes
import configparser
import webbrowser
from datetime import datetime
import requests
import pystray
from io import BytesIO
from PIL import Image
from tkinter import messagebox

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

class Win32PystrayIcon(pystray.Icon):
    WM_LBUTTONDBLCLK = 0x0203

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_double_click = kwargs.get('on_double_click', None)

    def _on_notify(self, wparam, lparam):
        super()._on_notify(wparam, lparam)
        if lparam == self.WM_LBUTTONDBLCLK and self.on_double_click:
            self.on_double_click()
            
class Overlay:
    def __init__(self):
        self.path = None
        self.version = "v"+"1.4"
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("10x10")
        self.root.configure(bg='black')
        self.overlay_alpha = 0.5
        self.root.attributes("-alpha", self.overlay_alpha)
        self.slider_window = None
        self.tray_icon = None
        self.autohide = False
        self.enable_overlay = True
        self.label = tk.Label(self.root, text="i stole this from wally :D",
                              fg="white", bg="black", font=('Times New Roman', 15, ''))
        self.label.pack(fill="both", expand=True)

        self.load_settings()

    def load_settings(self):
        """Load settings from an .ini file."""
        config = configparser.ConfigParser()
        settings_file = "settings.ini"
        if os.path.exists(settings_file):
            config.read(settings_file)
            self.overlay_alpha = float(config.get('Settings', 'overlay_alpha', fallback=0.5))
            self.autohide = config.getboolean('Settings', 'autohide', fallback=False)
            self.root.attributes("-alpha", self.overlay_alpha)  # Apply loaded transparency
        else:
            # Default settings if no settings file is found
            self.overlay_alpha = 0.5
            self.autohide = False

    def save_settings(self):
        """Save the overlay_alpha and autohide settings to an .ini file."""
        config = configparser.ConfigParser()

        # Check if the settings file exists; if not, create a new one
        settings_file = "settings.ini"
        if not os.path.exists(settings_file):
            with open(settings_file, 'w'): pass  # Create an empty file

        # Set default section and options for saving
        config.add_section('Settings')
        config.set('Settings', 'overlay_alpha', str(self.overlay_alpha))
        config.set('Settings', 'autohide', str(self.autohide))

        # Write to the settings.ini file
        with open(settings_file, 'w') as configfile:
            config.write(configfile)
            
        self.show_settings_saved_notification()
        
    def show_settings_saved_notification(self):
        """Display a notification window at the center of the screen."""
        # Create a new top-level window (notification window)
        notification_window = tk.Toplevel(self.root)
        notification_window.title("Settings Saved")
        notification_window.geometry("100x80+{}+{}".format(
            self.root.winfo_screenwidth() // 2 - 100,  # Center the window horizontally
            self.root.winfo_screenheight() // 2 - 50  # Center the window vertically
        ))
        notification_window.resizable(False, False)
        notification_window.configure(bg="white")
        notification_window.attributes("-topmost", True)

        label = tk.Label(notification_window, text="Settings Saved!", fg="black", bg="white")
        label.pack(pady=10)

        ok_button = tk.Button(notification_window, text="OK", command=notification_window.destroy)
        ok_button.pack()
        
        # Bind the Enter key to the OK button
        notification_window.bind("<Return>", lambda event: ok_button.invoke())

        notification_window.transient(self.root)
        notification_window.grab_set()
        notification_window.focus_force()
        
    def update_overlay(self, text, text_color):
        if self.enable_overlay:
            self.label.config(text=text, fg=text_color)
            self.root.update_idletasks()
            width = self.label.winfo_reqwidth() + 2
            self.root.geometry(f"{width}x40")

            hWindow = pywintypes.HANDLE(int(self.label.master.frame(), 16))
            exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
            win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    def toggle_visibility(self):
        """Show or hide the overlay window."""
        self.enable_overlay = not self.enable_overlay
        if self.enable_overlay:
            self.root.deiconify()
        else:
            self.root.withdraw()
            
    def toggle_autohide(self):
        self.autohide = not self.autohide
        
        self.tray_icon.menu = pystray.Menu(
            pystray.MenuItem("Show/Hide Overlay", lambda icon, item: self.toggle_visibility()),
            pystray.MenuItem("Transparency Slider", self.open_transparency_slider),
            pystray.MenuItem(f"Autohide: {'On (Minimizes to Tray)' if self.autohide else 'Off (Closes Scanner)'}", self.toggle_autohide),
            pystray.MenuItem("Check for Updates", self.check_updates),
            pystray.MenuItem("Save Settings", self.save_settings),
            pystray.MenuItem("Exit", self.exit_application)
        )

    def exit_application(self):
        """Exit the application."""
        self.tray_icon.stop()
        self.root.quit()
        os._exit(0)

    def create_tray_icon(self):
            """Create the system tray icon."""
            response = requests.get("https://static.wikia.nocookie.net/warframe/images/8/89/ThraxPlasm.png")
            image = Image.open(BytesIO(response.content))

            self.tray_icon = Win32PystrayIcon(
                name="Overlay Control",
                icon=image,
                title="Cascade Tile Scanner",
                menu=pystray.Menu(
                    pystray.MenuItem("Show/Hide Overlay", lambda icon, item: self.toggle_visibility()),
                    pystray.MenuItem("Transparency Slider", self.open_transparency_slider),
                    pystray.MenuItem(f"Autohide: {'On (Minimizes to Tray)' if self.autohide else 'Off (Closes Scanner)'}", self.toggle_autohide),
                    pystray.MenuItem("Check for Updates", self.check_updates),
                    pystray.MenuItem("Save Settings", self.save_settings),
                    pystray.MenuItem("Exit", self.exit_application)
                ),
                on_double_click=self.toggle_visibility  # Bind the double-click to toggle_visibility
            )
            
            self.tray_icon.run_detached()
    
    def check_updates(self):
        """Fetch the title of the latest release from a GitHub repository and show a popup."""
        url = "https://api.github.com/repos/tamawama/CascadeScanner/releases/latest"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            latest_version = data["name"]

            if latest_version != self.version:
                self.show_update_popup(latest_version)
            else:
                self.show_up_to_date_popup()

        except requests.RequestException as e:
            print(f"Error fetching updates: {e}")
            self.show_error_popup()

    def show_update_popup(self, latest_version):
        """Show a popup with a hyperlink to the latest release."""
        popup = tk.Toplevel()
        popup.title("Update Available")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.focus_force()
        
        # Message indicating the new version is available
        message = tk.Label(popup, text=f"A new version ({latest_version}) is available!", font=("Arial", 12))
        message.pack(pady=10)

        # Create a hyperlink-style label
        link = tk.Label(
            popup, 
            text="Click here to download the latest version", 
            font=("Arial", 10, "underline"), 
            fg="blue", 
            cursor="hand2"
        )
        link.pack(pady=10)
        # Bind the click event to open the URL in a web browser
        

        link.bind("<Button-1>", 
                  lambda e: (webbrowser.open_new("https://github.com/tamawama/CascadeScanner/releases/tag/compiled"),
                             close_button.invoke()
                  ))
        # Close button to dismiss the popup
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)
        
        popup.bind("<Return>", lambda event: close_button.invoke())
        
        popup.update_idletasks()

        # Centering to middle of the screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        window_width = popup.winfo_width()
        window_height = popup.winfo_height()

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        popup.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        
        def on_focus_out(event=None):
            if not popup.focus_get():
                popup.bell()
                popup.focus_force()
                
        popup.bind("<FocusOut>", on_focus_out)

    def show_up_to_date_popup(self):
        """Show a popup indicating the version is up-to-date."""
        popup = tk.Toplevel()
        popup.title("No Updates Available")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.focus_force()

        message = tk.Label(popup, text="Version is up-to-date!", font=("Arial", 12))
        message.pack(pady=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)
        
        popup.bind("<Return>", lambda event: close_button.invoke())
        
        popup.update_idletasks()
        
        # Centering to middle of the screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        window_width = popup.winfo_width()
        window_height = popup.winfo_height()

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        popup.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        def on_focus_out(event=None):
            if not popup.focus_get():
                popup.bell()
                popup.focus_force()
                
        popup.bind("<FocusOut>", on_focus_out)

    def show_error_popup(self):
        """Show a popup indicating an error occurred during the update check."""
        popup = tk.Toplevel()
        popup.title("Error")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.focus_force()

        message = tk.Label(popup, text="Error checking for updates.", font=("Arial", 12), fg="red")
        message.pack(pady=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)
        
        popup.bind("<Return>", lambda event: close_button.invoke())

        popup.update_idletasks()
        
        # Centering to middle of the screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        window_width = popup.winfo_width()
        window_height = popup.winfo_height()

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        popup.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        def on_focus_out(event=None):
            if not popup.focus_get():
                popup.bell()
                popup.focus_force()
                
        popup.bind("<FocusOut>", on_focus_out)
        
    def open_transparency_slider(self, icon, item):
        """Open a new window with a slider to adjust overlay transparency."""
        
        if self.slider_window is not None and self.slider_window.winfo_exists:
            self.slider_window.deiconify()
            self.slider_window.lift()
            return
        
        self.slider_window = tk.Toplevel(self.root)
        self.slider_window.title("Adjust Transparency")
        self.slider_window.resizable(False, False)
        self.slider_window.geometry("300x100")
        self.slider_window.protocol("WM_DELETE_WINDOW", self.hide_slider_window)

        label = tk.Label(self.slider_window, text="Transparency (0-1):")
        label.pack()

        slider = tk.Scale(self.slider_window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_transparency)
        slider.set(self.overlay_alpha)
        slider.pack()

    def hide_slider_window(self):
        """Hide the slider window instead of destroying it."""
        if self.slider_window is not None:
            self.slider_window.withdraw()

    def update_transparency(self, value):
        """Update the overlay's transparency based on slider value."""
        self.overlay_alpha = float(value)
        self.root.attributes("-alpha", self.overlay_alpha)

    def run(self):
        threading.Thread(target=self.track_tiles).start()
        self.create_tray_icon()
        self.update_overlay("Awaiting Cascade...", "red")
        self.root.mainloop()

    def track_tiles(self):
        global loadedMessage
        self.path = os.getenv('LOCALAPPDATA') + r'\Warframe\EE.log'

        if not os.path.isfile(self.path):
            print("Log file not found.")
            return

        color_map = {10: "red", 11: "yellow", 12: "green", 13: "cyan", 14: "magenta"}

        with open(self.path, encoding="utf8", errors="ignore") as logfile:
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
                    if self.slider_window:
                        self.hide_slider_window()
                        
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
                
                if attempts >= 1 and "Zariman Survival (Void Cascade): State Change: ENDLESS" in line:
                    if self.autohide:
                        self.toggle_visibility()
                    else:
                        self.exit_application()

if __name__ == '__main__':
    overlay = Overlay()
    overlay.run()