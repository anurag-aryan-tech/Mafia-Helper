import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from PIL import Image, ImageTk
from typing import Dict, List, Tuple, Callable, Optional
from dataclasses import dataclass


@dataclass
class StyleConfig:
    """Centralized styling configuration"""
    FG_COLOR = "#0B0F14"
    BD_COLOR = "#3A3F45"
    HOVER_COLOR = "#FF2A2A"
    TEXT_COLOR = "#E6EAF0"
    LABEL_COLOR = "#8392a3"
    BG_COLOR = "#152e2e"
    
    CORNER_RADIUS = 15
    BORDER_WIDTH = 10
    COMBO_BORDER_WIDTH = 5
    
    FONT_FAMILY = "Garamond"
    BUTTON_FONT_SIZE = 30
    LABEL_FONT_SIZE = 30
    COMBO_FONT_SIZE = 22
    DROPDOWN_FONT_SIZE = 18


@dataclass
class FrameConfig:
    """Configuration for frame creation"""
    name: str
    relheight: float
    relx: float = 0
    rely: float = 0
    relwidth: float = 1
    image_path: Optional[str] = None


class HoverEffect:
    """Handles hover effects for widgets"""
    
    @staticmethod
    def apply_to_widget(widget, hover_color: str, normal_color: str):
        """Apply hover effect to a widget"""
        widget.bind("<Enter>", lambda e: widget.configure(border_color=hover_color))
        widget.bind("<Leave>", lambda e: widget.configure(border_color=normal_color))


class RoleFrame:
    """Represents a single role's UI frame (Mafia, Sheriff, or Doctor)"""
    
    def __init__(self, parent, name: str, config: Dict, style: StyleConfig):
        self.name = name
        self.parent = parent
        self.style = style
        self.config = config
        
        self.frame = self._create_frame()
        self.phase_var = tk.StringVar(value=f"Phase {utils.nd_helper.night_phase}")
        self.dialogue_var = tk.StringVar()
        self.voted_var = tk.StringVar()
        
        self._setup_ui()
    
    def _create_frame(self) -> ctk.CTkFrame:
        """Create the main frame for this role"""
        frame = ctk.CTkFrame(
            self.parent,
            corner_radius=self.style.CORNER_RADIUS,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            bg_color=self.style.FG_COLOR,
            border_width=self.style.BORDER_WIDTH
        )
        frame.place(
            relx=self.config['relx'],
            rely=self.config['rely'],
            relwidth=self.config['relwidth'],
            relheight=self.config['relheight']
        )
        HoverEffect.apply_to_widget(frame, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return frame
    
    def _setup_ui(self):
        """Setup all UI elements for this role"""
        self._create_title_label()
        self.phase_combo = self._create_phase_combo()
        self.dial_vot_label = self._create_dialogue_label()
        self.dialogue_entry = self._create_dialogue_entry()
        self.voted_combo = self._create_voted_combo()
        self.copy_button = self._create_copy_button()
        self.previous_vote = None  # Track the previous vote for this role
    
    def _create_title_label(self):
        """Create the title label for the role"""
        is_mafia = self.name == "Mafia"
        rely = 0.05 if is_mafia else 0.1
        size = 35 if is_mafia else 30
        
        label = ctk.CTkLabel(
            master=self.frame,
            text=self.name,
            bg_color="transparent",
            text_color=self.style.LABEL_COLOR,
            font=ctk.CTkFont(self.style.FONT_FAMILY, size, "bold")
        )
        label.place(relx=0.05, rely=rely, relwidth=0.9, relheight=0.2)
    
    def _create_phase_combo(self) -> ctk.CTkComboBox:
        """Create the phase selection combobox"""
        is_mafia = self.name == "Mafia"
        rel_height = 0.125 if is_mafia else 0.2
        rel_y = 0.24 if is_mafia else 0.33
        
        combo = self._create_styled_combo(
            variable=self.phase_var,
            values=['Phase 1', 'Phase 2'],
            command=None  # Will be set externally
        )
        combo.place(relx=0.25, rely=rel_y, relwidth=0.55, relheight=rel_height)
        return combo
    
    def _create_dialogue_label(self) -> ctk.CTkLabel:
        """Create the dialogue/vote label"""
        is_mafia = self.name == "Mafia"
        rel_height = 0.1 if is_mafia else 0.15
        rel_y = 0.55 if is_mafia else 0.6
        size = 30 if is_mafia else 20
        
        label = ctk.CTkLabel(
            self.frame,
            text="Dialogue : ",
            fg_color='transparent',
            text_color=self.style.TEXT_COLOR,
            font=ctk.CTkFont(self.style.FONT_FAMILY, size, 'bold'),
            anchor="n"
        )
        label.place(relx=0.1, rely=rel_y, relwidth=0.3, relheight=rel_height)
        return label
    
    def _create_dialogue_entry(self) -> ctk.CTkEntry:
        """Create the dialogue entry field"""
        is_mafia = self.name == "Mafia"
        rel_height = 0.1 if is_mafia else 0.15
        rel_y = 0.55 if is_mafia else 0.6
        
        entry = ctk.CTkEntry(
            self.frame,
            corner_radius=7,
            border_width=self.style.COMBO_BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            fg_color=self.style.FG_COLOR,
            bg_color="transparent",
            text_color=self.style.TEXT_COLOR,
            font=(self.style.FONT_FAMILY, 18, 'bold'),
            justify='center',
            textvariable=self.dialogue_var
        )
        entry.place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
        HoverEffect.apply_to_widget(entry, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return entry
    
    def _create_voted_combo(self) -> ctk.CTkComboBox:
        """Create the voting combobox"""
        values = self._get_vote_values()
        self.voted_var.set("")
        
        combo = self._create_styled_combo(
            variable=self.voted_var,
            values=values,
            command=None  # Will be set externally
        )
        return combo
    
    def _get_vote_values(self) -> List[str]:
        """Get the list of players this role can vote for"""
        if self.name == "Mafia":
            # Mafia can only vote for non-mafia players
            return [name for name, _ in utils.db.players_list 
                    if name not in utils.db.mafias_list and name not in utils.db.eliminated_players]
        else:
            # Sheriff and Doctor can vote for anyone except eliminated players
            return [name for name, _ in utils.db.players_list 
                    if name not in utils.db.eliminated_players]
    
    def _create_copy_button(self) -> ctk.CTkButton:
        """Create the copy to clipboard button"""
        size = 30 if self.name == "Mafia" else 18
        
        button = ctk.CTkButton(
            self.frame,
            text="📋",
            command=None,  # Will be set externally
            fg_color="transparent",
            border_color="steelblue",
            text_color=self.style.TEXT_COLOR,
            border_width=3,
            font=(self.style.FONT_FAMILY, size, "bold")
        )
        button.place(relx=0.1, rely=0.75, relwidth=0.1, relheight=0.15)
        return button
    
    def _create_styled_combo(self, variable: tk.StringVar, values: List[str], 
                            command: Optional[Callable]) -> ctk.CTkComboBox:
        """Create a combobox with consistent styling"""
        combo = ctk.CTkComboBox(
            master=self.frame,
            corner_radius=self.style.CORNER_RADIUS,
            border_width=self.style.COMBO_BORDER_WIDTH,
            bg_color="transparent",
            font=(self.style.FONT_FAMILY, self.style.COMBO_FONT_SIZE, "bold"),
            text_color=self.style.TEXT_COLOR,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            button_color=self.style.BD_COLOR,
            button_hover_color=self.style.HOVER_COLOR,
            dropdown_fg_color=self.style.FG_COLOR,
            dropdown_text_color=self.style.TEXT_COLOR,
            dropdown_font=(self.style.FONT_FAMILY, self.style.DROPDOWN_FONT_SIZE, "bold"),
            variable=variable,
            values=values,
            command=command
        )
        HoverEffect.apply_to_widget(combo, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return combo
    
    def show_dialogue(self):
        """Show dialogue entry, hide voting combo"""
        if self.voted_combo.winfo_ismapped():
            self.voted_combo.place_forget()
        
        is_mafia = self.name == "Mafia"
        rel_height = 0.1 if is_mafia else 0.15
        rel_y = 0.55 if is_mafia else 0.6
        
        self.dialogue_entry.place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
        self.dial_vot_label.configure(text="Dialogue : ")
    
    def show_voting(self):
        """Show voting combo, hide dialogue entry"""
        if self.dialogue_entry.winfo_ismapped():
            self.dialogue_entry.place_forget()
        
        is_mafia = self.name == "Mafia"
        rel_height = 0.1 if is_mafia else 0.15
        rel_y = 0.55 if is_mafia else 0.6
        
        self.voted_combo.place(relx=0.425, rely=rel_y, relwidth=0.475, relheight=rel_height)
        self.dial_vot_label.configure(text="Vote : ")
    
    def update_phase_display(self):
        """Update the phase variable display"""
        self.phase_var.set(f"Phase {utils.nd_helper.night_phase}")


class MafiaControls:
    """Special controls specific to the Mafia frame"""
    
    def __init__(self, mafia_frame: RoleFrame, style: StyleConfig):
        self.mafia_frame = mafia_frame
        self.style = style
        # Filter out eliminated players from available speakers
        active_mafias = [name for name in utils.db.mafias_list 
                if name not in utils.db.eliminated_players]
        self.player_var = tk.StringVar(value=active_mafias[0] if active_mafias else "")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup mafia-specific UI elements"""
        self._create_speaker_label()
        self.player_combo = self._create_speaker_combo()
        self.next_button = self._create_next_button()
        self.day_button = self._create_done_button()
    
    def _create_speaker_label(self):
        """Create the speaker selection label"""
        label = ctk.CTkLabel(
            self.mafia_frame.frame,
            text="Speaker : ",
            fg_color='transparent',
            text_color=self.style.TEXT_COLOR,
            font=ctk.CTkFont(self.style.FONT_FAMILY, 30, 'bold')
        )
        label.place(relx=0.1, rely=0.425, relwidth=0.3, relheight=0.1)
    
    def _create_speaker_combo(self) -> ctk.CTkComboBox:
        """Create the speaker selection combobox"""
        # Filter out eliminated players from available speakers
        active_mafias = [name for name in utils.db.mafias_list 
                        if name not in utils.db.eliminated_players]
        combo = ctk.CTkComboBox(
            self.mafia_frame.frame,
            corner_radius=self.style.CORNER_RADIUS,
            border_width=self.style.COMBO_BORDER_WIDTH,
            bg_color="transparent",
            font=(self.style.FONT_FAMILY, self.style.COMBO_FONT_SIZE, "bold"),
            text_color=self.style.TEXT_COLOR,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            button_color=self.style.BD_COLOR,
            button_hover_color=self.style.HOVER_COLOR,
            dropdown_fg_color=self.style.FG_COLOR,
            dropdown_text_color=self.style.TEXT_COLOR,
            dropdown_font=(self.style.FONT_FAMILY, self.style.DROPDOWN_FONT_SIZE, "bold"),
            variable=self.player_var,
            values=active_mafias
        )
        combo.place(relx=0.425, rely=0.425, relwidth=0.475, relheight=0.1)
        HoverEffect.apply_to_widget(combo, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return combo
    
    def _create_next_button(self) -> ctk.CTkButton:
        """Create the NEXT button"""
        button = ctk.CTkButton(
            self.mafia_frame.frame,
            text="NEXT",
            command=None,  # Will be set externally
            fg_color="steelblue",
            border_color="blue",
            text_color=self.style.TEXT_COLOR,
            border_width=3,
            font=(self.style.FONT_FAMILY, self.style.BUTTON_FONT_SIZE, "bold")
        )
        button.place(relx=0.65, rely=0.75, relwidth=0.25, relheight=0.15)
        return button
    
    def _create_done_button(self) -> ctk.CTkButton:
        """Create the DAY button (hidden until night ends)"""
        button = ctk.CTkButton(
            self.mafia_frame.frame,
            text="DAY",
            command=None,  # Will be set externally
            fg_color="darkblue",
            border_color="blue",
            hover_color="blue",
            text_color=self.style.TEXT_COLOR,
            border_width=3,
            font=(self.style.FONT_FAMILY, self.style.BUTTON_FONT_SIZE, "bold")
        )
        button.place(relx=0.25, rely=0.75, relwidth=0.25, relheight=0.15)
        button.place_forget()  # Hide initially
        return button


class NightPhaseWindow:
    """Main window controller for Night Phase"""
    
    def __init__(self, master):
        self.master = master
        self.style = StyleConfig()
        self.window = self._create_window()
        self.frames = {}
        self.role_frames: Dict[str, RoleFrame] = {}
        self.mafia_controls: MafiaControls  # Will be initialized in _setup_mafia_controls
        
        self._setup_window()
        self._setup_background_frames()
        self._setup_role_frames()
        self._setup_mafia_controls()
        self._setup_event_handlers()
        self._initialize_ui_state()
    
    def _create_window(self) -> tk.Toplevel:
        """Create and configure the main window"""
        window = tk.Toplevel(self.master)
        window.transient(self.master)
        window.grab_set()
        window.title("Night Phase")
        window.config(bg=self.style.BG_COLOR)
        utils.initialize_windows(window)
        return window
    
    def _setup_window(self):
        """Setup window-specific configurations"""
        pass
    
    def _setup_background_frames(self):
        """Setup the title and body background frames"""
        configs = [
            FrameConfig("title_frame", 0.3, image_path="windows/night/night.png"),
            FrameConfig("body_frame", 0.7, image_path="images/background_image.png")
        ]
        
        last_height = 0
        for config in configs:
            frame = tk.Frame(self.window)
            frame.place(relx=0, rely=last_height, relwidth=1, relheight=config.relheight)
            last_height += config.relheight
            
            self.frames[config.name] = frame
            
            if config.image_path:
                self._setup_background_image(frame, config.image_path)
    
    def _setup_background_image(self, frame: tk.Frame, image_path: str):
        """Setup a resizable background image for a frame"""
        label = tk.Label(frame)
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        # Cache for optimization
        size_cache = {"width": 0, "height": 0}
        
        def on_configure(event):
            utils.image_config(event, label, size_cache, image_path)
        
        label.bind("<Configure>", on_configure)
    
    def _setup_role_frames(self):
        """Setup all three role frames"""
        configs = {
            "Mafia": {"relheight": 0.9, "relx": 0.05, "rely": 0.05, "relwidth": 0.45},
            "Sheriff": {"relheight": 0.45, "relx": 0.5, "rely": 0.05, "relwidth": 0.45},
            "Doctor": {"relheight": 0.45, "relx": 0.5, "rely": 0.5, "relwidth": 0.45}
        }
        
        for name, config in configs.items():
            role_frame = RoleFrame(
                self.frames["body_frame"],
                name,
                config,
                self.style
            )
            self.role_frames[name] = role_frame
    
    def _setup_mafia_controls(self):
        """Setup special controls for the Mafia frame"""
        self.mafia_controls = MafiaControls(
            self.role_frames["Mafia"],
            self.style
        )
    
    def _setup_event_handlers(self):
        """Setup all event handlers and callbacks"""
        # Phase change handler
        for role_frame in self.role_frames.values():
            role_frame.phase_combo.configure(command=self._on_phase_change)
        
        # Dialogue handlers
        for name, role_frame in self.role_frames.items():
            role_frame.dialogue_entry.bind(
                "<FocusOut>",
                lambda e, rf=role_frame: self._on_dialogue_change(rf)
            )
            role_frame.dialogue_entry.bind(
                "<Return>",
                lambda e, rf=role_frame: self._on_dialogue_change(rf)
            )
        
        # Vote handlers
        for name, role_frame in self.role_frames.items():
            role_frame.voted_combo.configure(
                command=lambda value, rf=role_frame: self._on_vote_change(rf, value.lower())
            )
        
        # Copy button handlers
        for name, role_frame in self.role_frames.items():
            role_frame.copy_button.configure(
                command=lambda n=name: self._copy_to_clipboard(n.lower())
            )
        
        # Mafia-specific handlers
        self.mafia_controls.next_button.configure(command=self._on_next_click)
        self.mafia_controls.day_button.configure(command=self._on_day_click)
    
    def _on_phase_change(self, event: str):
        """Handle phase change event"""
        if '1' in event:
            utils.nd_helper.night_phase = 1
            self.mafia_controls.next_button.configure(
                text="NEXT",
                command=self._on_next_click,
                fg_color="steelblue",
                border_color="blue",
                text_color=self.style.TEXT_COLOR,
                border_width=3,
                font=(self.style.FONT_FAMILY, self.style.BUTTON_FONT_SIZE, "bold")
            )
            # Hide day button in phase 1
            if self.mafia_controls.day_button.winfo_ismapped():
                self.mafia_controls.day_button.place_forget()
        elif '2' in event:
            utils.nd_helper.night_phase = 2
            if len(utils.db.mafias_list) == 1:
                self.mafia_controls.next_button.configure(
                    text="CHECK!",
                    fg_color="green",
                    border_color="lightgreen",
                    hover_color="darkgreen",
                    command=self._check_died
                )
        
        # Update all role frames
        for role_frame in self.role_frames.values():
            role_frame.update_phase_display()
        
        self._update_ui_for_phase()
    
    def _update_ui_for_phase(self):
        """Update UI elements based on current phase"""
        for role_frame in self.role_frames.values():
            if utils.nd_helper.night_phase == 1:
                role_frame.show_dialogue()
            else:
                role_frame.show_voting()
    
    def _on_dialogue_change(self, role_frame: RoleFrame):
        """Handle dialogue entry change"""
        speaker = self.mafia_controls.player_var.get()
        dialogue = role_frame.dialogue_var.get()
        utils.nd_helper.add_dialogue(speaker, dialogue)
    
    def _on_vote_change(self, role_frame: RoleFrame, new_vote: str):
        """Handle vote change - replace previous vote with new vote"""
        if not new_vote:  # Empty selection
            return
        
        # Doctor saves instead of voting
        if role_frame.name == "Doctor":
            utils.nd_helper.set_doctor_save(new_vote)
            role_frame.previous_vote = new_vote #type: ignore
            return
        
        # For other roles, handle regular votes
        # If there was a previous vote, remove it
        if role_frame.previous_vote:
            prev_vote_lower = role_frame.previous_vote.lower()
            if prev_vote_lower in utils.nd_helper.votes:
                utils.nd_helper.votes[prev_vote_lower] -= 1
                if utils.nd_helper.votes[prev_vote_lower] <= 0:
                    del utils.nd_helper.votes[prev_vote_lower]
        
        # Add the new vote
        utils.nd_helper.add_vote(new_vote)
        role_frame.previous_vote = new_vote # type: ignore
    
    def _on_next_click(self):
        """Handle NEXT button click - cycle through speakers and phases"""
        mafias_list = utils.db.mafias_list
        if not mafias_list:
            return
        
        current_speaker = self.mafia_controls.player_var.get()
        current_index = mafias_list.index(current_speaker) if current_speaker in mafias_list else 0
        
        # Check if this is the last speaker
        is_last_speaker = current_index == len(mafias_list) - 1
        is_last_second_speaker = current_index == len(mafias_list) - 2
        
        if utils.nd_helper.night_phase == 1:
            if is_last_speaker:
                # Last speaker in Phase 1: move to Phase 2 and reset to first speaker
                self._on_phase_change("2")
                self.mafia_controls.player_var.set(mafias_list[0])
            else:
                # Move to next speaker in Phase 1
                self.mafia_controls.player_var.set(mafias_list[current_index + 1])
        
        elif utils.nd_helper.night_phase == 2:
            if is_last_second_speaker:
                # Last speaker in Phase 2: change button to CHECK
                self.mafia_controls.next_button.configure(
                    text="CHECK!",
                    fg_color="green",
                    border_color="lightgreen",
                    hover_color="darkgreen",
                    command=self._check_died
                )
                self.mafia_controls.player_var.set(mafias_list[current_index + 1])
            else:
                # Move to next speaker in Phase 2
                self.mafia_controls.player_var.set(mafias_list[current_index + 1])
    
    def _check_died(self):
        """Check if the targeted player dies and show copy button"""
        target = utils.nd_helper.most_voted()[0]
        
        if target is None:
            utils.nd_helper.change_day_message("No one")
            message = "No one"
        else:
            # Check if doctor saved the target
            died = utils.nd_helper.check_died(target)
            
            if died:
                # Player actually died
                found_index = None
                for index, value in enumerate(utils.db.players_list):
                    if value[0].lower() == target.lower():
                        found_index = index
                        break
                if found_index is not None:
                    utils.db.players_list.pop(found_index)
                    utils.db.eliminated_players.append(target)
                utils.db.calculate_left()
                message = target
            else:
                # Doctor saved them
                message = "No one"
            
            utils.nd_helper.change_day_message(message)
        
        messagebox.showinfo("Night Result", f"{message} has died tonight. Day message updated.")
        
        # Change button to copy button
        if self.mafia_controls.next_button:
            self.mafia_controls.next_button.configure(
                text="📋",
                fg_color="steelblue",
                border_color="darkblue",
                command=lambda: self._copy_day_message()
            )
        
        # Show Day button
        if self.mafia_controls.day_button:
            self.mafia_controls.day_button.place(relx=0.25, rely=0.75, relwidth=0.25, relheight=0.15)
    
    def _on_day_click(self):
        """Handle DAY button click - increase day number and close window to return to day phase"""
        from windows.day.day_window import create_window as create_day_window
        
        # Increment night number when transitioning to day phase
        utils.nd_helper.increment_night()
        
        create_day_window(self.window.master) #type: ignore
        
        self.window.grab_release()
        self.window.transient(None)
        self.window.after(200, self.window.destroy)
    
    def _copy_day_message(self):
        """Copy the day message to clipboard"""
        day_message = utils.nd_helper.day_message
        self.window.clipboard_clear()
        self.window.clipboard_append(day_message)
        self.window.update()
        messagebox.showinfo("Copied", "Day message copied to clipboard!")
    
    def _copy_to_clipboard(self, role: str):
        """Copy the appropriate prompt to clipboard"""
        prompts = utils.db.prompts['night']
        
        if role == "mafia":
            prompt_data = prompts['mafia']
            dialogues = utils.nd_helper.get_dialogues()
        elif role == "sheriff":
            prompt_data = prompts['sheriff']
            dialogues = ""
        else:  # doctor
            prompt_data = prompts['doctor']
            dialogues = ""
        
        prompt = prompt_data['prompt']
        placeholders = prompts['mafia']['placeholders']
        
        current_actions = {
            "mafia": [
                "Discuss who you want to eliminate in 1-2 lines for your teammates!",
                "In just one word, select who do you want to eliminate!"
            ],
            "sheriff": [
                "Explain your thoughts about who you want to investigate!",
                "In just one word, select who do you want to investigate!"
            ],
            "doctor": [
                "Explain your thoughts about who you want to save!",
                "In just one word, select who do you want to save!"
            ]
        }
        
        updated_prompt = prompt.replace(
            placeholders['night_number'], str(utils.nd_helper.night_number)
        ).replace(
            placeholders['phase_number'], str(utils.nd_helper.night_phase)
        ).replace(
            placeholders['current_action'],
            current_actions[role][utils.nd_helper.night_phase - 1]
        ).replace(
            "[Dialogues]",
            f"### Dialogues:\n{dialogues}"
        )
        
        self.window.clipboard_clear()
        self.window.clipboard_append(updated_prompt)
        self.window.update()
    
    def _initialize_ui_state(self):
        """Initialize the UI to the correct state"""
        self._update_ui_for_phase()
        
        # If reopening in phase 2 with only 1 mafia, set button to CHECK
        if utils.nd_helper.night_phase == 2 and len(utils.db.mafias_list) == 1:
            self.mafia_controls.next_button.configure(
                text="CHECK!",
                fg_color="green",
                border_color="lightgreen",
                hover_color="darkgreen",
                command=self._check_died
            )


def create_window(master):
    """
    Create a toplevel window for the Night Phase prompts.
    This is the entry point that maintains backward compatibility.
    """
    NightPhaseWindow(master)