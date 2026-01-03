import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from PIL import Image, ImageTk

def create_window(master):
    """
    Create a window for prompts of each player.
    """
    # Create a toplevel window
    window = tk.Toplevel(master)
    window.transient(master)
    window.grab_set()
    window.title("Night Phase")
    window.config(bg="#152e2e")
    utils.initialize_windows(window)

    frames_config = [
        {
            "name": "title_frame",
            "relheight": 0.3,
            "image_path": "windows/night/night.png"
        },
        {
            "name": "body_frame",
            "relheight": 0.7,
            "image_path": "images/background_image.png"
        }
    ]

    frames = {}
    last_height = 0
    
    # Creating frames from config
    for frame_config in frames_config:
        frame_name = frame_config["name"]
        rel_height = frame_config["relheight"]
        image_path = frame_config["image_path"]

        frames[frame_name] = tk.Frame(window)
        frames[frame_name].place(relx=0, rely=last_height, relwidth=1, relheight=rel_height)
        last_height += rel_height

        # Label for the image
        label = tk.Label(frames[frame_name])
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=image_path: utils.image_config(event, lbl, last, pth))

    # Creating 3 frames for mafia, doctor, and sheriff actions
    action_frames_config = [
        {
            "name": "mafia_frame",
            "relheight": 0.9,
            "relx": 0.05,
            "rely": 0.05
        },
        {
            "name": "sheriff_frame",
            "relheight": 0.45,
            "relx" : 0.5,
            "rely": 0.05
        },
        {
            "name": "doctor_frame",
            "relheight": 0.45,
            "relx": 0.5,
            "rely": 0.5
        }
    ]

    fg_color = "#0B0F14"
    bd_color = "#3A3F45"
    hvr_color = "#FF2A2A"

    def on_enter(frame):
        frame.configure(border_color=hvr_color)
    def on_exit(frame):
        frame.configure(border_color=bd_color)

    # Creating action frames
    action_frames = {}

    for frame_config in action_frames_config:
        frame_name = frame_config["name"]
        rel_height = frame_config["relheight"]
        rel_x = frame_config.get("relx", 0)
        rel_y = frame_config.get("rely", 0)
        rel_width = 0.45

        action_frames[frame_name] = ctk.CTkFrame(
            frames["body_frame"],
            corner_radius=5,
            fg_color=fg_color,
            border_color=bd_color,
            bg_color=fg_color,
            border_width=10
        )
        action_frames[frame_name].place(relx=rel_x, rely=rel_y, relwidth=rel_width, relheight=rel_height)
        
        # Bind hover events
        action_frames[frame_name].bind("<Enter>", lambda e, f=action_frames[frame_name]: on_enter(f))
        action_frames[frame_name].bind("<Leave>", lambda e, f=action_frames[frame_name]: on_exit(f))

        # Add title to each frame
        title_text = ["Mafia", "Sheriff", "Doctor"]
        f_names = list(action_frames.values())
        
        for f_name, text in zip(f_names, title_text):
            if text == "Mafia":
                rely = 0.05
                size = 35
            else:
                rely = 0.1
                size = 30
            label = ctk.CTkLabel(
                master=f_name,
                text=text,
                bg_color="transparent",
                text_color="#8392a3",
                font=ctk.CTkFont("Garamond", size, "bold")
            )
            label.place(relx=0.05, rely=rely, relwidth=0.9, relheight=0.2)