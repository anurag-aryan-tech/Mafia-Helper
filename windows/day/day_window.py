import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from windows.prompts.prompts_window import ImageFrame, HoverEffects

@dataclass
class DayWindowConfig:
    BG_COLOR: str = "#152e2e"
    TITLE_IMAGE_PATH: str = "windows/day/day.png"
    BG_IMAGE_PATH: str = "images/background_image.png"

    TITLE_HEIGHT: float = 0.3
    @property
    def BODY_HEIGHT(self) -> float:
        return 1 - self.TITLE_HEIGHT


@dataclass
class StyleConfig:
    FG_COLOR: str = "#0B0F14"
    BD_COLOR: str = "#3A3F45"
    HOVER_COLOR: str = "#FF2A2A"
    BG_COLOR_FRAME: str = "#0F0A0A"
    TEXT_COLOR: str = "#E6EAF0"
    LABEL_BG_COLOR: str = "#152e2e"
    CORNER_RADIUS: int = 15
    BORDER_WIDTH: int = 7

    FONT_FAMILY: str = "Garamond"
    TEXT_SIZE: int = 30
    TEXT_SIZE_SMALL: int = 20

    TOTAL_FRAMES: int = 3
    FRAME_RATIO: str = "0.25:0.6:0.15"
    FRAMES_RELY_RELHEIGHT: List[Tuple[float, float]] = field(default_factory=list)

    COMBO_BORDER_WIDTH: int = 7
    COMBO_RADIUS: int = 15
    COMBO_TEXT_SIZE: int = 22

    def __post_init__(self) -> None:
        """Calculate relative y positions and heights for frames based on FRAME_RATIO"""
        try:
            ratios = list(map(float, self.FRAME_RATIO.split(":")))
        except ValueError:
            messagebox.showerror("Configuration Error", 
                            "Invalid FRAME_RATIO format. Using defaults.")
            self.FRAMES_RELY_RELHEIGHT = [(0.0, 0.33), (0.33, 0.33), (0.66, 0.34)]
            return
        
        e = ""
        if len(ratios) != self.TOTAL_FRAMES:
            e += f"FRAME_RATIO length {len(ratios)} does not match TOTAL_FRAMES {self.TOTAL_FRAMES}.\n"
        if any(r < 0 for r in ratios):
            e += "FRAME_RATIO values must be non-negative.\n"
        if abs(sum(ratios) - 1.0) > 0.0001:  # ✅ Tolerance-based comparison
            e += f"FRAME_RATIO values must sum to 1.0, got {sum(ratios):.6f}.\n"
        
        if e:
            messagebox.showerror("Configuration Error", e.strip())
            self.FRAMES_RELY_RELHEIGHT = [(0.0, 0.33), (0.33, 0.33), (0.66, 0.34)]
            return
        
        rely_relheights = []
        current_rely = 0.0
        for ratio in ratios:
            rely_relheights.append((current_rely, ratio))
            current_rely += ratio
        self.FRAMES_RELY_RELHEIGHT = rely_relheights
    


class DayPhaseWindow:
    def __init__(self, master: tk.Tk|tk.Toplevel) -> None:
        self.master = master
        self.window_config = DayWindowConfig()
        self.window = self._create_window()
        
        # Create shared InteractionFrame instance
        self.interaction_frame = InteractionFrame(self.window)

        self._setup_window_ui()

    def _setup_window_ui(self):
        self._create_image_frames()
        self._setup_action_frames()

    def _setup_action_frames(self):
        # Pass the shared interaction_frame instance
        self.selection_frame = SelectionFrame(self.body_frame, self.interaction_frame)
        self.prompt_frame = PromptFrame(self.body_frame, self.interaction_frame)
        self.footer_frame = FooterFrame(self.body_frame, self.interaction_frame)

    def _create_window(self):
        window = tk.Toplevel(self.master)
        window.title("Day Phase")
        window.config(bg=self.window_config.BG_COLOR)
        window.grab_set()
        window.transient(self.master)
        utils.initialize_windows(window)
        return window
    
    def _create_image_frames(self):
        title_height = self.window_config.TITLE_HEIGHT
        body_height = self.window_config.BODY_HEIGHT
        self.title_frame = ImageFrame(self.window, self.window_config.TITLE_IMAGE_PATH, 0, title_height)
        self.body_frame = ImageFrame(self.window, self.window_config.BG_IMAGE_PATH, title_height, body_height)

class FrameBase:
    def __init__(self):
        self.style = StyleConfig()
        self.rely_relheights = self.style.FRAMES_RELY_RELHEIGHT[:]

    def _create_frames(self, parent: tk.Frame|tk.Toplevel|ImageFrame, rely: float, relheight: float, relx: float = 0.0) -> tk.Frame:
        # Extract the actual frame if parent is ImageFrame
        actual_parent = parent.frame if isinstance(parent, ImageFrame) else parent
        
        frame = ctk.CTkFrame(
            actual_parent,
            fg_color=self.style.FG_COLOR,
            bg_color=self.style.BG_COLOR_FRAME,
            corner_radius=self.style.CORNER_RADIUS,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR
        )

        HoverEffects.apply_border_hover(
            frame, 
            self.style.HOVER_COLOR, 
            self.style.BD_COLOR
        )
        
        frame.place(relx=relx, rely=rely, relwidth=1-relx*2, relheight=relheight)
        return frame

    def _create_combobox(self, parent: tk.Frame|tk.Toplevel, variable: tk.StringVar|None=None, values: List[str]|None=None) -> ctk.CTkComboBox:
        combobox = ctk.CTkComboBox(
            parent,
            corner_radius=self.style.COMBO_RADIUS,
            border_width=self.style.COMBO_BORDER_WIDTH,
            bg_color="transparent",
            font=("Garamond", self.style.COMBO_TEXT_SIZE, "bold"),
            text_color=self.style.TEXT_COLOR,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            button_color=self.style.BD_COLOR,
            button_hover_color=self.style.HOVER_COLOR,
            dropdown_fg_color=self.style.FG_COLOR,
            dropdown_text_color=self.style.TEXT_COLOR,
            dropdown_font=("Garamond", 18, "bold"),
            variable=variable,
            values=values,
        )

        HoverEffects.apply_border_hover(
            combobox, 
            self.style.HOVER_COLOR, 
            self.style.BD_COLOR
        )

        return combobox
    
    def _create_border_frame(self, parent, relx: float, rely: float, relwidth: float, relheight: float) -> ctk.CTkFrame:
        border_frame = ctk.CTkFrame(
            parent,
            fg_color=self.style.FG_COLOR,
            bg_color=self.style.BG_COLOR_FRAME,
            corner_radius=self.style.CORNER_RADIUS,
            border_width=self.style.BORDER_WIDTH-2,
            border_color=self.style.BD_COLOR
        )

        HoverEffects.apply_border_hover(
            border_frame,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR
        )
        border_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return border_frame

class InteractionFrame(FrameBase):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.day_number = utils.nd_helper.day_number
        self.day_phase = utils.nd_helper.day_phase
        self.dialogue_vote_var = tk.StringVar()

        self.players_list = [x for x, _ in utils.db.players_list]
        self.day_prompts_dict = utils.db.prompts["day"]
        self.actual_prompt = self.day_prompts_dict["prompt"]
        self.placeholders = self.day_prompts_dict["placeholders"]

        self.phase_actions = [
            "Discuss: In one or two lines discuss your thoughts to others (speakers after you can see it in Phase 1),", 
            "Vote: In just one word vote out a player you suspect"
        ]
        self.current_action = self.phase_actions[self.day_phase - 1]
        self.current_prompt = ""
        self.prompt_var = tk.StringVar()

        self.player_var = tk.StringVar(value=f"{self.players_list[0]}")
        self.phase_var = tk.StringVar(value=f"Phase {self.day_phase}")

        self.dialogue_entry: ctk.CTkEntry|None = None
        self.vote_combobox: ctk.CTkComboBox|None = None
        self.vote_var = tk.StringVar()

        self.next_button: ctk.CTkButton|None = None
        self.player_died: str|None = None
        self.died_reason: str|None = None

        self._update_prompt()

    def _on_phase_change(self, current_phase: str):

        def set_first_player():
            if self.players_list:
                self.player_var.set(self.players_list[0])

        def set_phase_db(phase_str: str):
            try:
                phase_num = int(phase_str.split()[-1])
                utils.nd_helper.day_phase = phase_num
            except (ValueError, IndexError):
                messagebox.showerror("Error", f"Invalid phase selection: {phase_str}")

        set_first_player()
        set_phase_db(current_phase)
        self._update_prompt()
        self._place_dialogue_vote()
        utils.nd_helper.clear_dialogues()
        utils.nd_helper.clear_votes()

    def _on_player_change(self, _: str|None=None):
        self._update_prompt()

    def _update_prompt(self):
        self.day_phase = int((self.phase_var.get()).split()[-1])
        self.current_action = self.phase_actions[self.day_phase - 1]
        self.current_prompt = self.actual_prompt.replace(self.placeholders["day_number"], str(self.day_number)
            ).replace(self.placeholders["phase_number"], str(self.day_phase)
            ).replace(self.placeholders["current_action"], self.current_action
            ).replace(self.placeholders["dialogues"], utils.nd_helper.get_dialogues())
        self.prompt_var.set(self.current_prompt[:130] + "..." if len(self.current_prompt) > 130 else self.current_prompt)

    def _place_dialogue_vote(self) -> None:
        if self.vote_combobox and self.dialogue_entry:
            if self.day_phase == 1:
                self.dialogue_vote_var.set("Dialogue : ")
                if self.vote_combobox.winfo_ismapped():
                    self.vote_combobox.place_forget()
                self.dialogue_entry.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.6)
            else:
                self.dialogue_vote_var.set("Vote : ")
                if self.dialogue_entry.winfo_ismapped():
                    self.dialogue_entry.place_forget()
                self.vote_combobox.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.6)

    def _on_entering_dialogue(self, dialogue: str):
        utils.nd_helper.add_dialogue(self.player_var.get(), dialogue)
        if self.dialogue_entry:  # ✅ Check before access
            self.dialogue_entry.delete(0, tk.END)
        self._update_prompt()

    def _on_voting(self, votee: str):
        utils.nd_helper.add_vote(votee)

    def _copy_to_clipboard(self):
        prompt_text = self.current_prompt
        self.master.clipboard_clear()
        self.master.clipboard_append(prompt_text)
        self.master.update()  # now it stays on the clipboard after the window is closed

    def _check_died(self):
        results = utils.nd_helper.most_voted()
        self.player_died = results[0]
        self.died_reason = results[1]

    def _next_button_click(self, event=None):
        curr_player = self.player_var.get()
        players_pos = self.players_list.index(curr_player)

        if self.day_phase == 1:
            # Phase 1: Discussion phase
            if curr_player == self.players_list[-1]:
                # Last player in phase 1, move to phase 2
                self._on_phase_change("Phase 2")
                self.phase_var.set("Phase 2")
            else:
                # Move to next player
                self.player_var.set(self.players_list[players_pos + 1])
                return
        else:
            # Phase 2: Voting phase
            if curr_player == self.players_list[-2]:
                # Second to last player, move to last player
                self.player_var.set(self.players_list[-1])
                if self.next_button:
                    self.next_button.configure(fg_color="green", border_color="darkgreen", text="🔍")
            elif curr_player == self.players_list[-1]:
                self._check_died()
                self.current_prompt = f"""## Day Results
- **Day Number :** {self.day_number}
- **Player Died : {self.player_died}
- **Reason: {self.died_reason}"""
                # Last player voted, show copy prompt button
                if self.next_button:
                    self.next_button.configure(
                        fg_color="steelblue", 
                        border_color="darkblue", 
                        text="📋", 
                        command=self._copy_to_clipboard
                    )
            else:
                # Regular player in phase 2, move to next player
                self.player_var.set(self.players_list[players_pos + 1])
                return

        self._update_prompt()
                    

class SelectionFrame(FrameBase):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame, interaction_frame: InteractionFrame):
        super().__init__()
        self.parent = parent
        self.interaction = interaction_frame
        self.rely = self.rely_relheights[0][0]
        self.relheight = self.rely_relheights[0][1]

        self._setup_selection_frame()

    def _setup_selection_frame(self):
        self._create_selection_frame()
        self._place_combobox()

    def _create_selection_frame(self):
        self.selection_frame = self._create_frames(self.parent, self.rely, self.relheight)

    def _place_combobox(self):

        rely = 0.2
        relheight = 0.6

        def check_options(name: str, values: List[str]) -> None:
            # if not values or any(not v.strip() for v in values):
            if not values:
                messagebox.showerror("Configuration Error", f"No {name} found in database.")
                raise ValueError(f"No {name} found in database.")

        player_options = self.interaction.players_list
        check_options("players", player_options)

        self.player_combobox = self._create_combobox(self.selection_frame, self.interaction.player_var, player_options)
        self.player_combobox.place(relx=0.05, rely=rely, relwidth=0.4, relheight=relheight)
        self.player_combobox.configure(command=self.interaction._on_player_change)


        phase_options = [f"Phase {i}" for i in range(1, 3)]
        check_options("phases", phase_options)

        self.phase_combobox = self._create_combobox(self.selection_frame, self.interaction.phase_var, phase_options)
        self.phase_combobox.place(relx=0.55, rely=rely, relwidth=0.4, relheight=relheight)
        self.phase_combobox.configure(command=self.interaction._on_phase_change)

class PromptFrame(FrameBase):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame, interaction_frame: InteractionFrame):
        super().__init__()
        self.parent = parent
        self.interaction = interaction_frame
        self.rely = self.rely_relheights[1][0]
        self.relheight = self.rely_relheights[1][1]

        self._setup_prompt_frame()

    def _setup_prompt_frame(self):
        self._create_prompt_frame()
        self._setup_prompt_label()
        self._create_copy_button()

    def _create_prompt_frame(self):
        self.prompt_frame = self._create_frames(self.parent, self.rely, self.relheight)

    def _setup_prompt_label(self):
        # Border frame for the label
        border_frame = self._create_border_frame(self.prompt_frame, 0.09, 0.15, 0.75, 0.7)

        # Label inside border frame (no padding/margins)
        self.prompt_label = ctk.CTkLabel(
            border_frame,  # New master
            textvariable=self.interaction.prompt_var,
            font=(self.style.FONT_FAMILY, self.style.TEXT_SIZE_SMALL + 2, "bold"),
            text_color=self.style.TEXT_COLOR,
            justify="left",
            wraplength=650,  # Slight adjust for frame padding
            bg_color="transparent",  # Seamless with border frame
            anchor="nw",
            padx=10,
            pady=5
        )
        self.prompt_label.place(relx=0.03, rely=0.07, relwidth=0.94, relheight=0.86)
        HoverEffects.apply_border_hover(
            self.prompt_label,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR,
            widget_config=border_frame
        )

    def _create_copy_button(self):
        self.copy_button = ctk.CTkButton(
            self.prompt_frame,
            text="📋",
            font=(self.style.FONT_FAMILY, self.style.TEXT_SIZE+2, "bold"),
            fg_color=self.style.FG_COLOR,
            bg_color=self.style.BG_COLOR_FRAME,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS,
            command=self.interaction._copy_to_clipboard,
        )
        HoverEffects.apply_border_hover(
            self.copy_button,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR
        )
        self.copy_button.place(relx=0.85, rely=0.7, relwidth=0.1, relheight=0.25)


class FooterFrame(FrameBase):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame, interaction_frame: InteractionFrame):
        super().__init__()
        self.parent = parent
        self.interaction = interaction_frame
        self.rely = self.rely_relheights[2][0]
        self.relheight = self.rely_relheights[2][1]

        self._setup_footer_frame()

    def _setup_footer_frame(self):
        self._create_footer_frame()
        self._create_dialogue_vote_label()
        self._create_dialogue_entry()
        self._create_vote_combo()
        self.interaction._place_dialogue_vote()
        self._create_next_button()

    def _create_footer_frame(self):
        self.footer_frame = self._create_frames(self.parent, self.rely, self.relheight)

    def _create_dialogue_vote_label(self):
        self.interaction.dialogue_vote_var.set("Dialogue : " if self.interaction.day_phase == 1 else "Vote : ")
        # Border frame for the label
        border_frame = self._create_border_frame(self.footer_frame, 0.05, 0.2, 0.2, 0.6)

        # Label inside border frame (no padding/margins)
        self.dialogue_vote_label = ctk.CTkLabel(
            border_frame,  # New master
            textvariable=self.interaction.dialogue_vote_var,
            font=(self.style.FONT_FAMILY, self.style.TEXT_SIZE_SMALL, "bold"),
            text_color=self.style.TEXT_COLOR,
            justify="left",
            bg_color="transparent",  # Seamless with border frame
        )
        self.dialogue_vote_label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
        HoverEffects.apply_border_hover(
            self.dialogue_vote_label,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR,
            widget_config=border_frame
        )

    

    def _create_dialogue_entry(self):
        self.interaction.dialogue_entry = ctk.CTkEntry(
            self.footer_frame,
            font=(self.style.FONT_FAMILY, self.style.TEXT_SIZE_SMALL, "bold"),
            fg_color=self.style.FG_COLOR,
            bg_color=self.style.BG_COLOR_FRAME,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS-5,
            text_color=self.style.TEXT_COLOR,
        )
        HoverEffects.apply_border_hover(
            self.interaction.dialogue_entry,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR
        )
        def _on_dialogue_submit(event=None):
            if self.interaction.dialogue_entry:
                dialogue = self.interaction.dialogue_entry.get()
                self.interaction._on_entering_dialogue(dialogue)
        self.interaction.dialogue_entry.bind("<Return>", _on_dialogue_submit)

    def _create_vote_combo(self):
        self.interaction.vote_var.set(f"{self.interaction.players_list[0]}")
        self.interaction.vote_combobox = self._create_combobox(self.footer_frame, self.interaction.vote_var, self.interaction.players_list)
        self.interaction.vote_combobox.configure(command=self.interaction._on_voting)

    def _create_next_button(self):
        self.interaction.next_button = ctk.CTkButton(
            self.footer_frame,
            text="→",
            font=(self.style.FONT_FAMILY, self.style.TEXT_SIZE+2, "bold"),
            fg_color=self.style.FG_COLOR,
            bg_color=self.style.BG_COLOR_FRAME,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS,
            command=self.interaction._next_button_click,
        )
        HoverEffects.apply_border_hover(
            self.interaction.next_button,
            self.style.HOVER_COLOR,
            self.style.BD_COLOR
        )
        self.interaction.next_button.place(relx=0.85, rely=0.2, relwidth=0.1, relheight=0.6)

def create_window(master: tk.Tk | tk.Toplevel):
    DayPhaseWindow(master)