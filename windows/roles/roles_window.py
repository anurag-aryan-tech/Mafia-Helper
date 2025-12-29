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
        ("title_frame", "windows/roles/roles.png", 0, 0.3),
        ("body_frame", "images/background_image.png", 0.3, 0.7),
    ]

    for name, path, rel_y, rel_height in sections:

        # Frame for the title
        globals()[name] = frame = tk.Frame(window)
        frame.place(relx=0, rely=rel_y, relwidth=1, relheight=rel_height)

        # Label for the title image
        label = tk.Label(frame)
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=path: utils.image_config(event, lbl, last, pth))

    player_num = util.db.total_players
    mafia_num = util.db.total_mafias

    matrix = [[0]*3 for _ in range(4)]
    for i in range(player_num):
        index_1 = i//3
        index_2 = i%3
        matrix[index_1][index_2] = 1

    rows = (player_num+2)//3
    columns = 3

    for row in range(rows):
        body_frame.rowconfigure(row, weight=1)
    for column in range(columns):
        body_frame.columnconfigure(column, weight=1)

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == 1:
                globals()[f"c_{i}{j}"] = frame = ctk.CTkFrame(body_frame, bg_color= '#171717', fg_color='black', border_width=7, border_color="grey", corner_radius=15)
                frame.grid(row=i, column=j, sticky="nsew", padx= 10, pady= 10)