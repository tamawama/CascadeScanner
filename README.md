# Cascade Tile Search  

# DISCLAIMER: the scanner is inconsistently showing the wrong amount of exos, there's currently no way for me to fix this as it's not a scanner problem, but rather an ee.log problem, I will keep the release up but right now I would NOT recommend using the scanner.


This is a simple program to help you figure out exactly what tiles you have upon loading into a mission to help save time while rerolling. Simply run the script and the overlay will appear to the top left.  
When loading in to a mission, it will display the 3 main rooms in the map, along with how many exolizers will spawn in that room.  
Depending on the total amount of exolizers, the color of the HUD will change.  
![image](https://github.com/user-attachments/assets/060c7008-2b52-40a8-acad-469bce6547a3)  
10 or less Exolizers = Red  
11 Exolizers = Green  
12 Exolizers = Cyan  
13 Exolizers = Magenta  

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

