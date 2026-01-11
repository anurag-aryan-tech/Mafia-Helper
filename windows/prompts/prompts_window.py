import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Window layout configuration"""
    BG_COLOR = "#152e2e"
    TITLE_HEIGHT = 0.3
    BODY_HEIGHT = 0.7


@dataclass
class StyleConfig:
    """Styling configuration"""
    FG_COLOR = "#0B0F14"
    BD_COLOR = "#3A3F45"
    HOVER_COLOR = "#FF2A2A"
    BG_COLOR_FRAME = "#171717"
    TEXT_COLOR = "#E6EAF0"
    
    CORNER_RADIUS = 20
    BORDER_WIDTH = 7
    COMBO_BORDER_WIDTH = 5
    
    PREVIEW_LENGTH = 250


class ImageFrame:
    """Frame with dynamically resizing background image"""
    
    def __init__(self, parent: tk.Widget|tk.Toplevel, image_path: str, 
                 rely: float, relheight: float):
        self.parent = parent
        self.image_path = image_path
        self.last_size = {"width": 0, "height": 0}
        
        self.frame = tk.Frame(parent)
        self.frame.place(relx=0, rely=rely, relwidth=1, relheight=relheight)
        
        self.label = tk.Label(self.frame)
        self.label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.label.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        """Handle resize event"""
        utils.image_config(event, self.label, self.last_size, self.image_path)


class HoverEffects:
    """Utility class for applying hover effects"""
    
    @staticmethod
    def apply_border_hover(widget: ctk.CTkFrame|ctk.CTkComboBox|ctk.CTkButton|ctk.CTkLabel|ctk.CTkEntry, hover_color: str, normal_color: str, widget_config=None):
        if not widget_config:
            widget_config = widget
        """Apply border color hover effect"""
        widget.bind("<Enter>", lambda e: widget_config.configure(border_color=hover_color))
        widget.bind("<Leave>", lambda e: widget_config.configure(border_color=normal_color))

    @staticmethod
    def apply_text_hover(widget: ctk.CTkLabel, hover_color: str, normal_color: str):
        """Apply text color hover effect"""
        widget.bind("<Enter>", lambda e: widget.configure(text_color=hover_color))
        widget.bind("<Leave>", lambda e: widget.configure(text_color=normal_color))


class PromptGenerator:
    """Handles prompt generation with placeholder replacement"""
    
    def __init__(self, prompts_dict: Dict, players: Dict[str, str]):
        self.prompts_dict = prompts_dict
        self.players = players
        self.placeholders = prompts_dict['initial']['mafia']['placeholders']
    
    def generate_prompt(self, player_name: str) -> str:
        """Generate initial prompt for a player"""
        role = self.players[player_name]
        prompt = self.prompts_dict['initial'][role]['prompt']
        
        # Calculate player order
        player_order = " → ".join(self.players.keys())
        player_list = list(self.players.keys())
        player_index = player_list.index(player_name)
        
        # Replace common placeholders
        prompt = prompt.replace(
            self.placeholders['name'], player_name
        ).replace(
            self.placeholders['total_players'], str(utils.db.total_players)
        ).replace(
            self.placeholders['total_civilians'], 
            str(utils.db.total_players - utils.db.total_mafias - 2)
        ).replace(
            self.placeholders['total_mafias'], str(utils.db.total_mafias)
        ).replace(
            self.placeholders['position'], str(player_index + 1)
        ).replace(
            self.placeholders['player_order'], player_order
        ).replace(
            self.placeholders['players_before'], 
            str(player_list[:player_index])
        ).replace(
            self.placeholders['players_after'], 
            str(player_list[player_index + 1:])
        )
        
        # Mafia-specific placeholders
        if role == 'mafia':
            mafia_partners = self._get_mafia_partners(player_name)
            prompt = prompt.replace(
                self.placeholders['mafia_partners'], 
                mafia_partners
            )
        
        return prompt
    
    def _get_mafia_partners(self, player_name: str) -> str:
        """Get list of mafia partners for a player"""
        partners = [m for m in utils.db.mafias_list if m != player_name]
        return ', '.join(partners) if partners else 'None'


class PlayerSelectionFrame:
    """Frame for selecting which player to view"""
    
    def __init__(self, parent: tk.Frame, players: Dict[str, str], style: StyleConfig):
        self.parent = parent
        self.players = players
        self.style = style
        
        self.player_var = tk.StringVar(value=list(players.keys())[0])
        self.frame = self._create_frame()
        self._create_widgets()
    
    def _create_frame(self) -> ctk.CTkFrame:
        """Create the selection frame"""
        frame = ctk.CTkFrame(
            self.parent,
            bg_color=self.style.BG_COLOR_FRAME,
            fg_color=self.style.FG_COLOR,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS
        )
        frame.place(relx=0.025, relwidth=0.95, rely=0.05, relheight=0.25)
        HoverEffects.apply_border_hover(frame, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return frame
    
    def _create_widgets(self):
        """Create label and combo box"""
        # Label
        label = ctk.CTkLabel(
            self.frame,
            text="PLAYER : ",
            fg_color='transparent',
            text_color=self.style.TEXT_COLOR,
            font=ctk.CTkFont("Garamond", 40, 'bold')
        )
        label.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.6)
        HoverEffects.apply_text_hover(label, self.style.BD_COLOR, self.style.TEXT_COLOR)
        
        # ComboBox
        self.combo = ctk.CTkComboBox(
            self.frame,
            corner_radius=15,
            border_width=self.style.COMBO_BORDER_WIDTH,
            bg_color="transparent",
            font=("Garamond", 22, "bold"),
            text_color=self.style.TEXT_COLOR,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            button_color=self.style.BD_COLOR,
            button_hover_color=self.style.HOVER_COLOR,
            dropdown_fg_color=self.style.FG_COLOR,
            dropdown_text_color=self.style.TEXT_COLOR,
            dropdown_font=("Garamond", 18, "bold"),
            variable=self.player_var,
            values=list(self.players.keys())
        )
        self.combo.place(relx=0.4, rely=0.2, relwidth=0.4, relheight=0.6)
        HoverEffects.apply_border_hover(self.combo, self.style.HOVER_COLOR, self.style.BD_COLOR)
    
    def get_selected_player(self) -> str:
        """Get currently selected player"""
        return self.player_var.get()
    
    def set_command(self, command):
        """Set command for combo box selection"""
        self.combo.configure(command=command)


class PromptDisplayFrame:
    """Frame for displaying and interacting with prompts"""
    
    def __init__(self, parent: tk.Frame, style: StyleConfig):
        self.parent = parent
        self.style = style
        self.prompt_var = tk.StringVar()
        self.full_prompt = ""
        
        self.frame = self._create_frame()
        self._create_widgets()
    
    def _create_frame(self) -> ctk.CTkFrame:
        """Create the display frame"""
        frame = ctk.CTkFrame(
            self.parent,
            bg_color=self.style.BG_COLOR_FRAME,
            fg_color=self.style.FG_COLOR,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS
        )
        frame.place(relx=0.025, relwidth=0.95, rely=0.3, relheight=0.675)
        HoverEffects.apply_border_hover(frame, self.style.HOVER_COLOR, self.style.BD_COLOR)
        return frame
    
    def _create_widgets(self):
        """Create label and buttons"""
        # Prompt label
        self.label = ctk.CTkLabel(
            self.frame,
            textvariable=self.prompt_var,
            fg_color='transparent',
            text_color=self.style.TEXT_COLOR,
            font=ctk.CTkFont("Garamond", 18, "bold"),
            anchor="center",
            justify="left",
            wraplength=1000
        )
        self.label.place(relx=0.025, rely=0.1, relwidth=0.95, relheight=0.7)
        
        # Copy button
        self.copy_btn = ctk.CTkButton(
            self.frame,
            text="📋",
            command=None,  # Will be set externally
            fg_color="transparent",
            border_color="steelblue",
            text_color=self.style.TEXT_COLOR,
            border_width=3,
            font=("Garamond", 30, "bold")
        )
        self.copy_btn.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.15)
        
        # Next button
        self.next_btn = ctk.CTkButton(
            self.frame,
            text="NEXT",
            command=None,  # Will be set externally
            fg_color="steelblue",
            border_color="blue",
            text_color=self.style.TEXT_COLOR,
            border_width=3,
            font=("Garamond", 30, "bold")
        )
        self.next_btn.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.15)
    
    def set_prompt(self, full_prompt: str):
        """Set the prompt to display"""
        self.full_prompt = full_prompt
        preview = full_prompt[:StyleConfig.PREVIEW_LENGTH] + "..."
        self.prompt_var.set(preview)
    
    def get_full_prompt(self) -> str:
        """Get the full prompt text"""
        return self.full_prompt


class PromptsWindow:
    """Main window for viewing player prompts"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.window = self._create_window()
        self.style = StyleConfig()
        
        # Get player data
        self.players = {name: role for name, role in utils.db.players_list}
        self.player_names = list(self.players.keys())
        
        # Initialize prompt generator
        self.prompt_generator = PromptGenerator(utils.db.prompts, self.players)
        
        self._setup_frames()
        self._initialize_prompt()
        self._setup_event_handlers()
    
    def _create_window(self) -> tk.Toplevel:
        """Create and configure the toplevel window"""
        window = tk.Toplevel(self.master)
        window.transient(self.master)
        window.grab_set()
        window.title("Prompts")
        window.config(bg=WindowConfig.BG_COLOR)
        utils.initialize_windows(window)
        return window
    
    def _setup_frames(self):
        """Setup title and body frames"""
        # Title frame
        ImageFrame(
            self.window,
            "windows/prompts/prompts.png",
            0,
            WindowConfig.TITLE_HEIGHT
        )
        
        # Body frame
        body_image_frame = ImageFrame(
            self.window,
            "images/background_image.png",
            WindowConfig.TITLE_HEIGHT,
            WindowConfig.BODY_HEIGHT
        )
        self.body_frame = body_image_frame.frame
        
        # Selection and display frames
        self.selection_frame = PlayerSelectionFrame(
            self.body_frame,
            self.players,
            self.style
        )
        
        self.display_frame = PromptDisplayFrame(
            self.body_frame,
            self.style
        )
    
    def _initialize_prompt(self):
        """Initialize the prompt for the first player"""
        first_player = self.player_names[0]
        prompt = self.prompt_generator.generate_prompt(first_player)
        self.display_frame.set_prompt(prompt)
    
    def _setup_event_handlers(self):
        """Setup event handlers for buttons and selection"""
        self.selection_frame.set_command(self._on_player_change)
        self.display_frame.copy_btn.configure(command=self._copy_to_clipboard)
        self.display_frame.next_btn.configure(command=self._next_player)
    
    def _on_player_change(self, event=None):
        """Handle player selection change"""
        selected_player = self.selection_frame.get_selected_player()
        prompt = self.prompt_generator.generate_prompt(selected_player)
        self.display_frame.set_prompt(prompt)
    
    def _copy_to_clipboard(self):
        """Copy full prompt to clipboard"""
        full_prompt = self.display_frame.get_full_prompt()
        self.window.clipboard_clear()
        self.window.clipboard_append(full_prompt)
        self.window.update()
    
    def _next_player(self):
        """Move to next player or exit"""
        current_player = self.selection_frame.get_selected_player()
        
        if current_player == self.player_names[-1]:
            # Last player - ask to exit
            answer = messagebox.askokcancel(
                "Exit",
                "All players ended. Do you want to exit?"
            )
            if answer:
                self.window.after(100, self.window.destroy)
        else:
            # Move to next player
            current_index = self.player_names.index(current_player)
            next_player = self.player_names[current_index + 1]
            self.selection_frame.player_var.set(next_player)
            
            # Update button if next is last player
            if next_player == self.player_names[-1]:
                self.display_frame.next_btn.configure(
                    text="EXIT",
                    fg_color="green",
                    border_color='lightgreen',
                    hover_color="darkgreen"
                )
            
            self._on_player_change()


def create_window(master: tk.Tk):
    """
    Create a window for viewing player prompts.
    Entry point maintaining backward compatibility.
    """
    PromptsWindow(master)