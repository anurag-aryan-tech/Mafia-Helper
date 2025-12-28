import tkinter as tk
import customtkinter as ctk
from utils import Utilities, util
from PIL import Image, ImageTk

utils = Utilities()


def create_window(master):
    """
    Create a window for total number of players.
    """
    # Create a toplevel window
    window = tk.Toplevel(master)
    window.transient(master)
    window.grab_set()
    window.title("Total Players")
    window.config(bg="#152e2e")
    utils.initialize_windows(window)

    # Path to the title image
    title_path = "windows/total_players/total_players.png"
    last = {"width": 0, "height": 0}

    # Frame for the title
    title_frame = tk.Frame(window)
    title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)

    # Label for the title image
    title_label = tk.Label(title_frame)
    title_label.place(relx=0, rely=0, relheight=1, relwidth=1)
    title_label.bind("<Configure>", lambda event: utils.image_config(event, title_label, last, title_path))

    # Open the background image
    bg_image = Image.open("images/background_image.png")

    # Create frames for the main content
    main_frame = tk.Frame(window)
    main_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

    # Label for the background image
    bg_photo = ImageTk.PhotoImage(bg_image.resize((1400, 650)))
    bg_label = tk.Label(main_frame, image=bg_photo)
    bg_label.place(relx=0, rely=0, relheight=1, relwidth=1)
    bg_label.image = bg_photo

    # Define colors and dimensions for the frames
    fg = "#062929"
    bg = "#0C0C0A"
    bd_color = "#1e6363"
    rel_x, rel_y = 0.05, 0.05
    rel_width, rel_height = 0.4, 0.75

    # Create the player and mafia frames
    total_player_frame = ctk.CTkFrame(main_frame,
            corner_radius=20,
            border_width=5,
            border_color=bd_color,
            bg_color=bg,
            fg_color=fg)
    total_player_frame.place(relx=rel_x, rely=rel_y, relwidth=rel_width, relheight=rel_height)
    total_player_frame.grid_propagate(False)

    total_mafia_frame = ctk.CTkFrame(main_frame,
            corner_radius=20,
            border_width=5,
            border_color=bd_color,
            bg_color=bg,
            fg_color=fg)
    total_mafia_frame.place(relx=rel_x+0.45, rely=rel_y, relwidth=rel_width, relheight=rel_height)
    total_mafia_frame.grid_propagate(False)

    # Define the layout for the frames
    total_columns = 4
    total_rows = 3
    for column in range(total_columns):
        total_player_frame.columnconfigure(column, weight=1)
        total_mafia_frame.columnconfigure(column, weight=1)
    for row in range(total_rows):
        total_player_frame.rowconfigure(row, weight=1)
        total_mafia_frame.rowconfigure(row, weight=1)

    # Create labels for the player and mafia frames
    player_title_label = ctk.CTkLabel(total_player_frame, text="PLAYERS", fg_color="transparent", text_color="#D6643E", font=ctk.CTkFont("Garamond", 40, "bold", underline=True), pady=10)
    player_title_label.grid(column=0, row=0, columnspan=4, sticky="nsew", padx=8, pady=(30, 10))

    mafia_title_label = ctk.CTkLabel(total_mafia_frame, text="MAFIAS", fg_color="transparent", text_color="#D6643E", font=ctk.CTkFont("Garamond", 40, "bold", underline=True), pady=10)
    mafia_title_label.grid(column=0, row=0, columnspan=4, sticky="nsew", padx=8, pady=(30, 10))

    # Create a list of player numbers
    player_range = [str(n) for n in range(4, 12)]

    # Create StringVars for the total player and total mafia values
    total_player = tk.StringVar(value=f"{util.db.total_players}")
    total_mafia = tk.StringVar(value=f"{util.db.total_mafias}")

    # Define colors and dimensions for combo boxes
    fg = "#062929"
    bd_color = "#1e6363"
    height = 65

    # Create combo boxes for the player and mafia inputs
    combo_attr = [("player_input", total_player_frame, player_range, total_player, "normal"),
                ("mafia_input", total_mafia_frame, None, total_mafia, "disabled")]

    for name, frame, values, variable, state in combo_attr:
        globals()[name] = combo_box = ctk.CTkComboBox(frame,
                corner_radius=15,
                border_width=5,
                bg_color="transparent",
                values=values,
                font=("Garamond", 27, "bold"),
                fg_color=fg,
                border_color=bd_color,
                button_color=bd_color,
                dropdown_fg_color=fg,
                dropdown_text_color="white",
                dropdown_font=("Garamond", 22, "bold"),
                width=height*5,
                height=height,
                variable=variable,
                state=state)
        combo_box.grid(column=0, row=1, columnspan=4, padx=40, pady=(10, 100))

    # Function to enable the mafia input based on the player input
    # This function is called when the player input combobox value is changed
    def enable_mafia_input(event=None):
        # Get the player input value and convert it to an integer
        player_num = int(total_player.get())
        # Change the total number of players in the database
        util.db.change_player_num(player_num)
        # Get the mafia input value and convert it to an integer
        mafia_num = int(total_mafia.get())
        # Calculate the maximum number of mafias based on the player number
        if player_num % 2 == 0:
            mafia_limit = (player_num // 2)
        else:
            mafia_limit = player_num//2+1

        # If the mafia input value is greater than or equal to the mafia limit,
        # set it to the mafia limit - 1 and update the database
        if mafia_num >= mafia_limit:
                total_mafia.set(str(mafia_limit-1))
                util.db.change_mafia_num(mafia_limit-1)

        # Update the values of the mafia input combobox based on the mafia limit
        mafia_input.configure(values= [str(n) for n in range(1, mafia_limit)])
        # If the player number is 4 (minimum number of players), disable the mafia input combobox
        if player_num == 4:
            mafia_input.configure(state= 'disabled')
        else:
            mafia_input.configure(state= 'normal')

    # Configure the player input combobox to call the enable_mafia_input function when its value is changed
    player_input.configure(command= lambda event=None: enable_mafia_input(event))
    # Configure the mafia input combobox to call the change_mafia_num function of the database when its value is changed
    mafia_input.configure(command= lambda event=None: util.db.change_mafia_num(int(total_mafia.get())))

    def close_window():
        window.destroy()

    normal = Image.open("windows/total_players/done_button/frame_1.png")
    pressed = Image.open("windows/total_players/done_button/frame_2.png")
    done_button = utils.Custom_Buttons(main_frame, normal, pressed, bg="#0e0d0d", command=lambda: window.after(100, close_window))
    done_button.place(rely= 0.83, relheight= 0.15, relx= 0.4, relwidth= 0.15)
