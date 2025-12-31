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
    window.title("Prompts")
    window.config(bg="#152e2e")
    utils.initialize_windows(window)

    sections = [
        ("title_frame", "windows/prompts/prompts.png", 0, 0.3),
        ("body_frame", "images/background_image.png", 0.3, 0.7),
    ]

    frames = {}

    for name, path, rel_y, rel_height in sections:

        # Frame for the title
        frames[name] = frame = tk.Frame(window)
        frame.place(relx=0, rely=rel_y, relwidth=1, relheight=rel_height)

        # Label for the title image
        label = tk.Label(frame)
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=path: utils.image_config(event, lbl, last, pth))

    fg_color = "#0B0F14"
    bd_color = "#3A3F45"
    hvr_color = "#FF2A2A"

    def on_enter(frame, attr=None):
        if not attr:
            frame.configure(border_color=hvr_color)
        else:
            frame.configure(text_color=bd_color)
    def on_exit(frame, attr=None):
        if not attr:
            frame.configure(border_color=bd_color)
        else:
            frame.configure(text_color="#E6EAF0")

    selection_frame = ctk.CTkFrame(frames["body_frame"], bg_color= '#171717', fg_color=fg_color, border_width=7, border_color=bd_color, corner_radius=20)
    
    selection_frame.bind("<Enter>", lambda event=None, f=selection_frame: on_enter(frame=f))
    selection_frame.bind("<Leave>", lambda event=None, f=selection_frame: on_exit(frame=f))

    prompts_frame = ctk.CTkFrame(frames["body_frame"], bg_color= '#171717', fg_color=fg_color, border_width=7, border_color=bd_color, corner_radius=20)
    
    prompts_frame.bind("<Enter>", lambda event=None, f=prompts_frame: on_enter(frame=f))
    prompts_frame.bind("<Leave>", lambda event=None, f=prompts_frame: on_exit(frame=f))

    prompts_frame.place(relx= 0.025, relwidth= 0.95, rely=0.3, relheight= 0.675)
    selection_frame.place(relx= 0.025, relwidth= 0.95, rely=0.05, relheight= 0.25)

    player_label = ctk.CTkLabel(selection_frame, text="PLAYER : ", fg_color='transparent', text_color='#E6EAF0', font=ctk.CTkFont("Garamond", 40, 'bold'))
    player_label.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.6)

    player_label.bind("<Enter>", lambda event=None, f=player_label: on_enter(frame=f, attr=True))
    player_label.bind("<Leave>", lambda event=None, f=player_label: on_exit(frame=f, attr=True))

    values = []
    for name, _ in utils.db.players_list:
        values.append(name)

    player_var = tk.StringVar(value=values[0])
    player_combo = ctk.CTkComboBox(selection_frame,
            corner_radius=15,
            border_width=5,
            bg_color="transparent", 
            font=("Garamond", 22, "bold"), 
            text_color="#E6EAF0", 
            fg_color=fg_color, 
            border_color=bd_color,
            button_color=bd_color, 
            button_hover_color=hvr_color, 
            dropdown_fg_color=fg_color, 
            dropdown_text_color="#E6EAF0", 
            dropdown_font=("Garamond", 18, "bold"), 
            variable=player_var, 
            values=values)
    player_combo.place(relx=0.4, rely=0.2, relwidth=0.4, relheight=0.6)
    player_combo.bind("<Enter>", lambda event=None, f=player_combo: on_enter(frame=f))
    player_combo.bind("<Leave>", lambda event=None, f=player_combo: on_exit(frame=f))