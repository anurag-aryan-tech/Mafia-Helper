import tkinter as tk
import customtkinter as ctk
from utils import Utilities, util
from PIL import Image, ImageTk

utils = Utilities()

def create_window(master):
    """
    Create a window for roles of each player.
    """
    # Create a toplevel window
    window = tk.Toplevel(master)
    window.transient(master)
    window.grab_set()
    window.title("Roles")
    window.config(bg="#152e2e")
    utils.initialize_windows(window)

    