# Cascade Tile Search  

# DISCLAIMER: the scanner is inconsistently showing the wrong amount of exos, there's currently no way for me to fix this as it's not a scanner problem, but rather an ee.log problem. As long as you don't mind having -1 exo than the count shows, it seems like the log is consistently generating only 1 exo that doesn't exist, so if you don't mind a potential 533 on what should be a 543, then the scanner is mostly alright to use.


This is a simple program to help you figure out exactly what tiles you have upon loading into a mission to help save time while rerolling. Simply run the script and the overlay will appear to the top left.  
When loading in to a mission it will display the amount of exolizers you have.  
Depending on the total amount of exolizers, the color of the HUD will change.  
![python_l3n9Ru5h3m](https://github.com/user-attachments/assets/1605fc82-e7b2-4feb-9519-e61d4f6d53b4)  
10 or less Exolizers = Red  
11 Exolizers = Yellow  
12 Exolizers = Green  
13 Exolizers = Cyan  
14 Exolizers = Magenta  

Feel free to compile it youself with pyinstaller, or just run it through python directly!

### Installation
Download and extract the ZIP from [releases](https://github.com/tamawama/CascadeScanner/releases) or clone this repository and run it yourself through Python.

### Compiling / Running it yourself
if this doesn't work, feel free to ask about it
1. Install [Python](https://www.python.org/downloads/) (Add it to the PATH when prompted to)
2. Download this repository (press "<> Code", Download ZIP) and extract the files.   
or `git clone https://github.com/tamawama/CascadeScanner.git`
3. Open up the folder in your terminal (right click inside your folder -> "Open in Terminal")
4. Run `pip install -r requirements.txt`
5. Run `py CascadeTileScanner.py` to launch it  
   or run `pip install pyinstaller` then `pyinstaller CascadeTileScanner.py` to compile the script to an EXE.  
   The compiled .exe should be inside the `dist` folder

