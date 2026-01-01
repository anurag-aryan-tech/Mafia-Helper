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

    players = {}
    for name, role in utils.db.players_list:
        players[name] = role

    values = list(players.keys())
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

    prompts_dict = utils.db.prompts
    placeholders = prompts_dict['initial']['mafia']['placeholders']
    player_order = ""
    for name in players:
        player_order += name + "→ "
    player_order = player_order.rstrip("→ ")

    initial_prompt = prompts_dict['initial'][players[player_var.get()]]['prompt']
    initial_prompt = initial_prompt.replace(placeholders['name'], player_var.get()).replace(placeholders['total_players'], str(utils.db.total_players)).replace(placeholders['total_civilians'], str(utils.db.total_players-utils.db.total_mafias-2)).replace(placeholders['total_mafias'], str(utils.db.total_mafias)).replace(placeholders['position'], str(list(players.keys()).index(player_var.get())+1)).replace(placeholders['player_order'], player_order).replace(placeholders['players_before'], str(list(list(players.keys())[:list(players.keys()).index(player_var.get())]))).replace(placeholders['players_after'], str(list(list(players.keys())[list(players.keys()).index(player_var.get())+1:])))
    if players[player_var.get()] == 'mafia':
        m_p = utils.db.mafias_list
        m_p.remove(player_var.get())
        if not m_p:
            m_p = 'None'
        else:
            m_p = ', '.join(m_p)
        initial_prompt = initial_prompt.replace(placeholders['mafia_partners'], m_p)

    real_prompt = initial_prompt

    curr_prompt = tk.StringVar(value=real_prompt[:250]+"...")
    prompts_label = ctk.CTkLabel(prompts_frame, textvariable=curr_prompt, fg_color='transparent', text_color='#E6EAF0', font=ctk.CTkFont("Garamond", 18, "bold"), anchor="center", justify="left", wraplength=1000)
    prompts_label.place(relx=0.025, rely=0.1, relwidth=0.95, relheight=0.7)

    def copy_to_clipboard(event=None):
        nonlocal real_prompt
        window.clipboard_clear()
        window.clipboard_append(real_prompt)
        window.update()

    def next_prompt(event=None):
        current_player = player_var.get()
        if current_player == values[-1]:
            answer = messagebox.askokcancel("Exit", "All players ended, Do you want to exit?")
            if answer:
                window.after(100, window.destroy)
                return
        elif current_player in values:
            player_pos = values.index(current_player)
            next_player = values[player_pos+1]
            player_var.set(next_player)
            if next_player == values[-1]:
                next_btn.configure(text="EXIT", fg_color="green", border_color='lightgreen', hover_color="darkgreen")
            change_player()
            

    def change_player(event=None):
        nonlocal real_prompt
        new_prompt = prompts_dict['initial'][players[player_var.get()]]['prompt']
        new_prompt = new_prompt.replace(placeholders['name'], player_var.get()).replace(placeholders['total_players'], str(utils.db.total_players)).replace(placeholders['total_civilians'], str(utils.db.total_players-utils.db.total_mafias-2)).replace(placeholders['total_mafias'], str(utils.db.total_mafias)).replace(placeholders['position'], str(list(players.keys()).index(player_var.get())+1)).replace(placeholders['player_order'], player_order).replace(placeholders['players_before'], str(list(list(players.keys())[:list(players.keys()).index(player_var.get())]))).replace(placeholders['players_after'], str(list(list(players.keys())[list(players.keys()).index(player_var.get())+1:])))
        if players[player_var.get()] == 'mafia':
            m_p = utils.db.mafias_list[:]
            m_p.remove(player_var.get())
            if not m_p:
                m_p = 'None'
            else:
                m_p = ', '.join(m_p)
            new_prompt = new_prompt.replace(placeholders['mafia_partners'], m_p)
        real_prompt = new_prompt
        curr_prompt.set(new_prompt[:250]+"...")

    player_combo.configure(command=change_player)
    copy_btn = ctk.CTkButton(prompts_frame, text="📋", command=copy_to_clipboard, fg_color="transparent", border_color="steelblue", text_color="#E6EAF0", border_width=3, font=("Garamond", 30, "bold"))
    copy_btn.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.15)

    next_btn = ctk.CTkButton(prompts_frame, text="NEXT", command=next_prompt, fg_color="steelblue", border_color="blue", text_color="#E6EAF0", border_width=3, font=("Garamond", 30, "bold"))
    next_btn.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.15)