import Desktop
import gui
import threading

def main():
    
    GUIThread = gui.GUI(800,700,"snus")
    GUIThread.idle()
    
if __name__ == "__main__":
    main()