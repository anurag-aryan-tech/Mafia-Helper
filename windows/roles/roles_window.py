import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from PIL import Image, ImageTk

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
        ("title_frame", "windows/roles/roles.png", 0, 0.2),
        ("body_frame", "images/background_image.png", 0.2, 0.7),
    ]

    for name, path, rel_y, rel_height in sections:

        # Frame for the title
        globals()[name] = frame = tk.Frame(window)
        frame.place(relx=0, rely=rel_y, relwidth=1, relheight=rel_height)

        # Label for the title image
        label = tk.Label(frame)
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=path: utils.image_config(event, lbl, last, pth))

    footer_frame = ctk.CTkFrame(window, fg_color="#171717")
    footer_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

    player_num = utils.db.total_players
    mafia_num = utils.db.total_mafias
    villager_num = player_num-mafia_num-2

    role_count = {
        "" : 0,
        "villager" : 0,
        "mafia" : 0,
        "sheriff" : 0,
        "doctor" : 0,
    }
    for _, role in utils.db.players_list:
        role_count[role] += 1
    values = [""]
    if role_count['villager'] < villager_num:
        values.append("Villager")
    if role_count['mafia'] < mafia_num:
        values.append("Mafia")
    if role_count['sheriff'] == 0:
        values.append("Sheriff")
    if role_count['doctor'] == 0:
        values.append("Doctor")

    rows = (player_num+2)//3
    columns = 3

    matrix = [[0]*3 for _ in range(rows)]
    for i in range(player_num):
        index_1 = i//3
        index_2 = i%3
        matrix[index_1][index_2] = 1

    for row in range(rows):
        body_frame.rowconfigure(row, weight=1)
    for column in range(columns):
        body_frame.columnconfigure(column, weight=1)

    fg_color = "#0B0F14"
    bd_color = "#3A3F45"
    hvr_color = "#FF2A2A"

    def on_enter(frame):
        frame.configure(border_color=hvr_color)
    def on_exit(frame):
        frame.configure(border_color=bd_color)

    frame_names = []
    name_n_role = {}
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == 1:
                globals()[f"c_{i}{j}"] = frame = ctk.CTkFrame(body_frame, bg_color= '#171717', fg_color=fg_color, border_width=7, border_color=bd_color, corner_radius=15)
                frame_names.append((f"c_{i}{j}", frame))
                frame.grid(row=i, column=j, sticky="nsew", padx= 10, pady= 10)
                frame.bind("<Enter>", lambda event=None, f=frame: on_enter(frame=f))
                frame.bind("<Leave>", lambda event=None, f=frame: on_exit(frame=f))

    def role_command(event, fn, rb: ctk.CTkComboBox):
        row = int(fn[2])
        column = int(fn[3])
        position = row*3 + column + 1
        try:
            utils.db.change_players_list(name_n_role[fn][0].get(), event.lower(), position)
        except Exception as e:
            print(f"Error updating role: {e}")
            messagebox.showerror("Error", f"Failed to update role: {e}")
            rb.set("")  # Reset the combobox to empty state
            return

        role_count = {
            "" : 0,
            "villager" : 0,
            "mafia" : 0,
            "sheriff" : 0,
            "doctor" : 0,
        }
        for _, role in utils.db.players_list:
            role_count[role] += 1
        values = [""]
        if role_count['villager'] < villager_num:
            values.append("Villager")
        if role_count['mafia'] < mafia_num:
            values.append("Mafia")
        if role_count['sheriff'] == 0:
            values.append("Sheriff")
        if role_count['doctor'] == 0:
            values.append("Doctor")

        for r_box in role_boxes:
            r_box.configure(values= values)


        

    pos = 0
    role_boxes = []
    for f_name, frame in frame_names:
        top_label = ctk.CTkLabel(frame, text=f"Speaker {pos+1}", font=ctk.CTkFont("Garamond", 35, 'bold'), bg_color='transparent', fg_color='transparent', text_color="#8392a3")
        top_label.place(relx=0.05, rely=0.1, relheight=0.2, relwidth=0.9)

        name_var = tk.StringVar(value=utils.db.players_list[pos][0])
        role_var = tk.StringVar(value=utils.db.players_list[pos][1].title())

        name_entry = ctk.CTkEntry(frame, corner_radius=7, border_width=5, border_color=bd_color, fg_color=fg_color, bg_color="transparent", text_color="#E6EAF0", font=("Garamond", 18, 'bold'), justify='center', textvariable=name_var)
        name_entry.place(relx=0.3, relwidth=0.6, rely=0.4, relheight=0.2)
        
        name_label = ctk.CTkLabel(frame, text="NAME : ", fg_color='transparent', text_color="#545c66", font=ctk.CTkFont("Garamond", 17, 'bold'))
        name_label.place(relx=0.05, relwidth=0.2, rely=0.4, relheight=0.2)

        role_box = ctk.CTkComboBox(frame,
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
                variable=role_var,
                values=values)
        role_box.configure(command= lambda event=None, fn=f_name, rb=role_box: role_command(event, fn, rb))
        role_box.place(relx=0.3, relwidth=0.6, rely=0.7, relheight=0.2)
        role_label = ctk.CTkLabel(frame, text="ROLE : ", fg_color='transparent', text_color="#545c66", font=ctk.CTkFont("Garamond", 17, 'bold'))
        role_label.place(relx=0.05, relwidth=0.2, rely=0.7, relheight=0.2)

        name_n_role[f_name] = (name_var, role_var)
        role_boxes.append(role_box)

        position = pos + 1  # because pos is 0-based

        def on_name_commit(event=None, p=position, nv=name_var):
            utils.db.change_player_name(nv.get(), p)

        name_entry.bind("<FocusOut>", on_name_commit)
        
        name_entry.bind("<Enter>", lambda event=None, f=name_entry: on_enter(frame=f))
        name_entry.bind("<Leave>", lambda event=None, f=name_entry: on_exit(frame=f))
        role_box.bind("<Enter>", lambda event=None, f=role_box: on_enter(frame=f))
        role_box.bind("<Leave>", lambda event=None, f=role_box: on_exit(frame=f))
        pos += 1

    def done_command(event=None):
        window.focus_set()
        window.update_idletasks()
        for name, role in utils.db.players_list:
            if not name or not role:
                messagebox.showwarning("Missing Values", "Some 'Names' and/or 'Roles' are missing!!")
                return
        answer = messagebox.askokcancel("Procced", "Action cannot be undone! If proceeded, you cannot change names, roles and numbers of player!")
        if answer:
            utils.db.change_first_disable()
            window.destroy()

    normal = Image.open("windows/total_players/done_button/frame_1.png")
    pressed = Image.open("windows/total_players/done_button/frame_2.png")
    done_button = utils.Custom_Buttons(footer_frame, normal, pressed, bg="#171717", command= lambda: window.after(100, done_command))
    done_button.place(rely = 0.05, relheight= 0.9, relx= 0.3, relwidth= 0.4)

        