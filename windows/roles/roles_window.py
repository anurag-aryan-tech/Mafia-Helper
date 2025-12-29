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

    sections = [
        ("title_frame", "windows/total_players/total_players.png", 0, 0.3),
        ("body_frame", "images/background_image.png", 0.3, 0.6),
        ("footer_frame", "images/background_image.png", 0.9, 0.1)
    ]

    for name, path, rel_y, rel_height in sections:

        # Frame for the title
        globals()[name] = frame = tk.Frame(window)
        frame.place(relx=0, rely=rel_y, relwidth=1, relheight=rel_height)

        # Label for the title image
        label = tk.Label(frame)
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=path: utils.image_config(event, lbl, last, pth))

    # # Path to the title image
    # title_path = "windows/total_players/total_players.png"
    # last = {"width": 0, "height": 0}

    # # Frame for the title
    # title_frame = tk.Frame(window)
    # title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)

    # # Label for the title image
    # title_label = tk.Label(title_frame)
    # title_label.place(relx=0, rely=0, relheight=1, relwidth=1)
    # title_label.bind("<Configure>", lambda event: utils.image_config(event, title_label, last, title_path))

    # bg_path = "images/background_image.png"
    # last_body = {"width": 0, "height": 0}

    # # Frame for the title
    # body_frame = tk.Frame(window)
    # body_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.6)

    # # Label for the title image
    # body_label = tk.Label(body_frame)
    # body_label.place(relx=0, rely=0, relheight=1, relwidth=1)
    # body_label.bind("<Configure>", lambda event: utils.image_config(event, body_label, last_body, bg_path))