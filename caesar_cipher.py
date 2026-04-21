"""
caesar_cipher.py — entry point. Creates the root window, shows the splash, then hands off to MainWindow.

Caesar Cipher — Version 3.0
"""
import tkinter as tk

from constants import BG
from splash import show_entry_dialogue
from main_window import MainWindow


def main():
    root = tk.Tk()
    root.title("Caesar Cipher")
    root.resizable(True, True)
    root.minsize(760, 540)
    root.configure(bg=BG)
    root.withdraw()   # hide until splash is dismissed

    start_mode = show_entry_dialogue(root)

    if start_mode in ("exit", ""):
        root.destroy()
        return

    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    MainWindow(root, start_mode)
    root.mainloop()


if __name__ == "__main__":
    main()
