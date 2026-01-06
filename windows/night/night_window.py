import tkinter as tk
from tkinter import messagebox  # imported for potential dialogs (not used in this file)
import customtkinter as ctk
from utils import utils  # project utilities: db, nd_helper, image helpers, window initialization
from PIL import Image, ImageTk  # imported for image handling (not directly used here but kept for compatibility)

def create_window(master):
    """
    Create a toplevel window for the Night Phase prompts.
    All UI elements are created inside this window and hooked to utils (db and nd_helper).
    """
    # Create a modal toplevel window tied to the master window
    window = tk.Toplevel(master)
    window.transient(master)
    window.grab_set()
    window.title("Night Phase")
    window.config(bg="#152e2e")
    utils.initialize_windows(window)  # project-specific window initialization (size, position etc.)

    # Configuration for the top title image frame and the body background frame
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
    
    # Create and place the frames defined in frames_config.
    # Each frame gets a Label covering the entire frame for showing a background image.
    # The label binds to <Configure> to handle resizing via utils.image_config.
    for frame_config in frames_config:
        frame_name = frame_config["name"]
        rel_height = frame_config["relheight"]
        image_path = frame_config["image_path"]

        frames[frame_name] = tk.Frame(window)
        frames[frame_name].place(relx=0, rely=last_height, relwidth=1, relheight=rel_height)
        last_height += rel_height

        # Label used as a background image placeholder/stretchable canvas
        label = tk.Label(frames[frame_name])
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        # Bind reconfigure to update the image via the util helper.
        # Lambda captures label and image_path. "last" dict caches previous size to optimize re-scaling.
        label.bind("<Configure>", lambda event, lbl=label, last={"width": 0, "height": 0}, pth=image_path: utils.image_config(event, lbl, last, pth))

    # Configuration for three action frames inside the body: mafia, sheriff, doctor
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

    # Visual constants for frames and hover colors
    fg_color = "#0B0F14"
    bd_color = "#3A3F45"
    hvr_color = "#FF2A2A"

    # Hover handlers to change the border color of CTkFrame on mouse enter/leave
    def on_enter(frame):
        frame.configure(border_color=hvr_color)
    def on_exit(frame):
        frame.configure(border_color=bd_color)

    # Create the customtkinter frames for actions with consistent styling and placement.
    action_frames = {}

    for frame_config in action_frames_config:
        frame_name = frame_config["name"]
        rel_height = frame_config["relheight"]
        rel_x = frame_config.get("relx", 0)
        rel_y = frame_config.get("rely", 0)
        rel_width = 0.45  # fixed width fraction for action frames

        action_frames[frame_name] = ctk.CTkFrame(
            frames["body_frame"],
            corner_radius=15,
            fg_color=fg_color,
            border_color=bd_color,
            bg_color=fg_color,
            border_width=10
        )
        action_frames[frame_name].place(relx=rel_x, rely=rel_y, relwidth=rel_width, relheight=rel_height)
        
        # Bind hover events to change frame border color for visual feedback.
        # Lambda captures the specific frame instance.
        action_frames[frame_name].bind("<Enter>", lambda e, f=action_frames[frame_name]: on_enter(f))
        action_frames[frame_name].bind("<Leave>", lambda e, f=action_frames[frame_name]: on_exit(f))

    def ui_changer():
        """Toggle between dialogue and voting UI based on current phase."""
        for text in title_text:
            rel_height = 0.1 if text == "Mafia" else 0.15
            rel_y = 0.55 if text == "Mafia" else 0.6
            
            if utils.nd_helper.night_phase == 1:
                # Show dialogue entry
                if voted_combos[text.lower()][0].winfo_ismapped():
                    voted_combos[text.lower()][0].place_forget()
                dialogue_entries[text.lower()][0].place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
                dial_vot_labels[text.lower()].configure(text="Dialogue : ")
            else:
                # Show voting combo
                if dialogue_entries[text.lower()][0].winfo_ismapped():
                    dialogue_entries[text.lower()][0].place_forget()
                voted_combos[text.lower()][0].place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
                dial_vot_labels[text.lower()].configure(text="Vote : ")

    def check_died(event=None):
        """Check if the targeted player dies considering the doctor's save."""
        target = utils.nd_helper.most_voted()[0]
        if target is None:
            utils.nd_helper.change_day_message("No one")
        else:
            died = utils.nd_helper.check_died(target)
            if not died:
                utils.nd_helper.change_day_message("No one")
            else:
                utils.nd_helper.change_day_message(target)

    # Titles for the three action frames in the same order as action_frames.values()
    title_text = ["Mafia", "Sheriff", "Doctor"]
    f_names = list(action_frames.values())

    # Phase selection values (Phase 1 or Phase 2) and containers to hold the StringVar and boxes
    phases = ['Phase 1', 'Phase 2']
    phase_vars = {}
    phase_boxes = {}

    # change_phase receives a value (event-like) and updates the shared nd_helper.night_phase
    # Also updates the visible phase StringVars for each role box.
    def change_phase(event):
        if '1' in event:
            utils.nd_helper.night_phase = 1
            next_btn.configure(text="NEXT", command=next_prompt, fg_color="steelblue", border_color="blue", text_color="#E6EAF0", border_width=3, font=("Garamond", 30, "bold"))
        elif '2' in event:
            utils.nd_helper.night_phase = 2
            next_btn.configure(text="CHECK!", fg_color="green", border_color="lightgreen", hover_color="darkgreen")
        for var in phase_vars.values():
            var.set(value=f"Phase {utils.nd_helper.night_phase}")
        ui_changer()
        
    # Populate each action frame with a title label and a phase selection combobox.
    # There is slightly different layout/styling for Mafia vs Sheriff/Doctor.
    for f_name, text in zip(f_names, title_text):
        if text == "Mafia":
            rely = 0.05
            size = 35
            rel_height=0.125
            rel_y = 0.24
        else:
            rely = 0.1
            size = 30
            rel_height=0.2
            rel_y = 0.33
        # Title label for the role
        label = ctk.CTkLabel(
                master=f_name,
                text=text,
                bg_color="transparent",
                text_color="#8392a3",
                font=ctk.CTkFont("Garamond", size, "bold")
            )
        label.place(relx=0.05, rely=rely, relwidth=0.9, relheight=0.2)

        # Each role maintains a StringVar representing the currently selected phase.
        phase_var = tk.StringVar(value=f"Phase {utils.nd_helper.night_phase}")
        phase_vars[text] = phase_var

        # ComboBox for selecting Phase 1/2 for this role. Hooks the change_phase command.
        phase_box = ctk.CTkComboBox(master=f_name,
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
            variable=phase_var, 
            values=phases,
            command=change_phase)
        phase_box.place(relx=0.25, rely=rel_y, relwidth=0.55, relheight=rel_height)
        # Hover feedback for the combo box itself (uses the same on_enter/on_exit handlers)
        phase_box.bind("<Enter>", lambda event=None, f=phase_box: on_enter(frame=f))
        phase_box.bind("<Leave>", lambda event=None, f=phase_box: on_exit(frame=f))
        phase_boxes[text] = phase_box

    # --- Mafia frame specific widgets follow ---

    # Label indicating the current speaking player in the mafia frame
    player_label = ctk.CTkLabel(action_frames["mafia_frame"], text="Speaker : ", fg_color='transparent', text_color='#E6EAF0', font=ctk.CTkFont("Garamond", 30, 'bold'))
    player_label.place(relx=0.1, rely=0.425, relwidth=0.3, relheight=0.1)

    # Values for the mafia speaker combobox come from utils.db.mafias_list
    values = utils.db.mafias_list
    player_var = tk.StringVar(value=values[0])

    # Combobox to select which mafia member is speaking
    player_combo = ctk.CTkComboBox(action_frames["mafia_frame"],
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
    player_combo.bind("<Enter>", lambda event=None, f=player_combo: on_enter(frame=f))
    player_combo.bind("<Leave>", lambda event=None, f=player_combo: on_exit(frame=f))
    player_combo.place(relx=0.425, rely=0.425, relwidth=0.475, relheight=0.1)

    # Dialogue label and entry for mafia to add their spoken lines
    dial_vot_labels = {}
    dialogue_entries = {}
    for text in title_text:
        if text == "Mafia":
            rel_height=0.1
            rel_y = 0.55
            size = 30
        else:
            rel_height=0.15
            rel_y = 0.6
            size = 20
        dial_vot_label = ctk.CTkLabel(action_frames[f"{text.lower()}_frame"], text="Dialogue : ", fg_color='transparent', text_color='#E6EAF0', font=ctk.CTkFont("Garamond", size, 'bold'), anchor="n")
        dial_vot_label.place(relx=0.1, rely=rel_y, relwidth=0.3, relheight=rel_height)
        dial_vot_labels[text.lower()] = dial_vot_label

        dialogue_var = tk.StringVar()
        dialogue_entry = ctk.CTkEntry(action_frames[f"{text.lower()}_frame"], corner_radius=7, border_width=5, border_color=bd_color, fg_color=fg_color, bg_color="transparent", text_color="#E6EAF0", font=("Garamond", 18, 'bold'), justify='center', textvariable=dialogue_var)
        dialogue_entry.place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
        dialogue_entries[text.lower()] = (dialogue_entry, dialogue_var)

        # Bind focus out and return key to add dialogue via nd_helper
        dialogue_entry.bind("<FocusOut>", lambda event=None, var=dialogue_var: utils.nd_helper.add_dialogue(player_var.get(), var.get()))
        dialogue_entry.bind("<Return>", lambda event=None, var=dialogue_var: utils.nd_helper.add_dialogue(player_var.get(), var.get()))

        dialogue_entry.bind("<Enter>", lambda event=None, f=dialogue_entry: on_enter(frame=f))
        dialogue_entry.bind("<Leave>", lambda event=None, f=dialogue_entry: on_exit(frame=f))


    # Helper to add a vote (lowercases the provided name before passing to nd_helper)
    def add_vote(event):
        utils.nd_helper.add_vote(event.lower())


    # Build the list of vote targets: all players who are not mafias
    mafia_values = []
    general_values = []
    for name, _ in utils.db.players_list:
        if name not in utils.db.mafias_list:
            mafia_values.append(name)
        general_values.append(name)
    voted_combos = {}

    for text in title_text:
        if text == "Mafia":
            values = mafia_values
        else:
            values = general_values
        voted_var = tk.StringVar(value=values[0])
        voted_combo = ctk.CTkComboBox(action_frames[f"{text.lower()}_frame"],
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
                variable=voted_var, 
                values=values,
                command=add_vote)
        voted_combo.bind("<Enter>", lambda event=None, f=voted_combo: on_enter(frame=f))
        voted_combo.bind("<Leave>", lambda event=None, f=voted_combo: on_exit(frame=f))
        voted_combos[f"{text.lower()}"] = [voted_combo, voted_var]

    # Retrieve mafia prompt template and placeholders from the project DB
    mafia_prompt = utils.db.prompts['night']['mafia']['prompt']
    shriff_prompt = utils.db.prompts['night']['sheriff']['prompt']
    doctor_prompt = utils.db.prompts['night']['doctor']['prompt']
    placeholders = utils.db.prompts['night']['mafia']['placeholders']

    # Copy the constructed prompt to the clipboard. The prompt is built using placeholders
    # plus current dialogues from nd_helper.get_dialogues().
    def copy_to_clipboard(event:str):
        if event is None:
            event = "mafia"
            prompt = mafia_prompt
        elif event.lower() == "mafia":
            dialogues = utils.nd_helper.get_dialogues()
            prompt = mafia_prompt
        else:
            if event.lower() == "sheriff":
                prompt = shriff_prompt
            else:
                prompt = doctor_prompt
            dialogues = ""

        current_actions = {"mafia": ["Discuss who you want to eliminate in 1-2 lines for your teammates!", "In just one word, select who do you want to eliminate!"],
                           "sheriff": ["Explain your thoughts about who you want to investigate!", "In just one word, select who do you want to investigate!"],
                           "doctor": ["Explain your thoughts about who you want to save!", "In just one word, select who do you want to save!"]}
        updated_prompt = prompt.replace(placeholders['night_number'], str(utils.nd_helper.night_number)).replace(placeholders['phase_number'], str(utils.nd_helper.night_phase)).replace(placeholders['current_action'], current_actions[event.lower()][utils.nd_helper.night_phase-1]).replace("[Dialogues]", f"### Dialogues:\n{dialogues}")
        window.clipboard_clear()
        window.clipboard_append(updated_prompt)
        window.update()

    ui_changer()

    # Handler for the NEXT button: progresses mafia UI from discussion to vote if only one mafia remains.
    # Uses and updates UI elements and nd_helper state accordingly.
    def next_prompt(event=None):
        current_player = player_var.get()
        nonlocal mafia_prompt
        if len(utils.db.mafias_list) == 1:
            # If we're in phase 1, switch to phase 2, clear dialogues and change UI to voting mode.
            if utils.nd_helper.night_phase == 1:
                change_phase("2")
                next_btn.configure(text="CHECK!", fg_color="green", border_color="lightgreen", hover_color="darkgreen", command=check_died)

    # Copy-to-clipboard button placed inside the mafia frame
    for text in title_text:
        size = 30 if text == "Mafia" else 18
        copy_btn = ctk.CTkButton(action_frames[f"{text.lower()}_frame"], text="📋", command=lambda event=text.lower(): copy_to_clipboard(event), fg_color="transparent", border_color="steelblue", text_color="#E6EAF0", border_width=3, font=("Garamond", size, "bold"))
        copy_btn.place(relx=0.1, rely=0.75, relwidth=0.1, relheight=0.15)

    # NEXT button that advances the mafia prompt flow; wired to next_prompt
    next_btn = ctk.CTkButton(action_frames["mafia_frame"], text="NEXT", command=next_prompt, fg_color="steelblue", border_color="blue", text_color="#E6EAF0", border_width=3, font=("Garamond", 30, "bold"))
    next_btn.place(relx=0.65, rely=0.75, relwidth=0.25, relheight=0.15)