import tkinter as tk
import customtkinter as ctk
from utils import utils
from PIL import Image, ImageTk
from typing import Tuple
from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Window styling configuration"""
    BG_COLOR = "#152e2e"
    TITLE_HEIGHT = 0.3
    MAIN_HEIGHT = 0.7


@dataclass
class FrameConfig:
    """Frame styling configuration"""
    FG_COLOR = "#062929"
    BG_COLOR = "#0C0C0A"
    BORDER_COLOR = "#1e6363"
    CORNER_RADIUS = 20
    BORDER_WIDTH = 5
    REL_X = 0.05
    REL_Y = 0.05
    REL_WIDTH = 0.4
    REL_HEIGHT = 0.75


@dataclass
class ComboConfig:
    """ComboBox styling configuration"""
    CORNER_RADIUS = 15
    BORDER_WIDTH = 5
    FONT_SIZE = 27
    DROPDOWN_FONT_SIZE = 22
    HEIGHT = 65


class BackgroundFrame:
    """Manages a frame with a background image"""
    
    def __init__(self, parent, image_path: str, 
                 relx: float, rely: float, relwidth: float, relheight: float):
        self.parent = parent
        self.image_path = image_path
        self.frame = tk.Frame(parent)
        self.frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        self.bg_photo = None  # Keep reference to prevent garbage collection
        self._setup_background()
    
    def _setup_background(self):
        """Setup the background image"""
        bg_image = Image.open(self.image_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image.resize((1400, 650)))
        self.bg_label = tk.Label(self.frame, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relheight=1, relwidth=1)


class TitleFrame:
    """Manages the title frame with dynamic image resizing"""
    
    def __init__(self, parent: tk.Toplevel, image_path: str):
        self.parent = parent
        self.image_path = image_path
        self.last_size = {"width": 0, "height": 0}
        
        self.frame = tk.Frame(parent)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=WindowConfig.TITLE_HEIGHT)
        
        self.label = tk.Label(self.frame)
        self.label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.label.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        """Handle resize event"""
        utils.image_config(event, self.label, self.last_size, self.image_path)


class PlayerMafiaFrame:
    """Manages a single player/mafia input frame"""
    
    def __init__(self, parent: tk.Widget, title: str, 
                 relx: float, values: list|None = None, initial_value: str = "1",
                 state: str = "normal"):
        self.parent = parent
        self.title = title
        self.values = values
        self.variable = tk.StringVar(value=initial_value)
        
        self.frame = self._create_frame(relx)
        self._setup_grid()
        self._create_title_label()
        self.combo_box = self._create_combo_box(state)
    
    def _create_frame(self, relx: float) -> ctk.CTkFrame:
        """Create the main frame"""
        frame = ctk.CTkFrame(
            self.parent,
            corner_radius=FrameConfig.CORNER_RADIUS,
            border_width=FrameConfig.BORDER_WIDTH,
            border_color=FrameConfig.BORDER_COLOR,
            bg_color=FrameConfig.BG_COLOR,
            fg_color=FrameConfig.FG_COLOR
        )
        frame.place(
            relx=relx,
            rely=FrameConfig.REL_Y,
            relwidth=FrameConfig.REL_WIDTH,
            relheight=FrameConfig.REL_HEIGHT
        )
        frame.grid_propagate(False)
        return frame
    
    def _setup_grid(self):
        """Configure grid layout"""
        for col in range(4):
            self.frame.columnconfigure(col, weight=1)
        for row in range(3):
            self.frame.rowconfigure(row, weight=1)
    
    def _create_title_label(self):
        """Create the title label"""
        label = ctk.CTkLabel(
            self.frame,
            text=self.title,
            fg_color="transparent",
            text_color="#D6643E",
            font=ctk.CTkFont("Garamond", 40, "bold", underline=True),
            pady=10
        )
        label.grid(column=0, row=0, columnspan=4, sticky="nsew", padx=8, pady=(30, 10))
    
    def _create_combo_box(self, state: str) -> ctk.CTkComboBox:
        """Create the combo box"""
        combo = ctk.CTkComboBox(
            self.frame,
            corner_radius=ComboConfig.CORNER_RADIUS,
            border_width=ComboConfig.BORDER_WIDTH,
            bg_color="transparent",
            values=self.values,
            font=("Garamond", ComboConfig.FONT_SIZE, "bold"),
            fg_color=FrameConfig.FG_COLOR,
            border_color=FrameConfig.BORDER_COLOR,
            button_color=FrameConfig.BORDER_COLOR,
            dropdown_fg_color=FrameConfig.FG_COLOR,
            dropdown_text_color="white",
            dropdown_font=("Garamond", ComboConfig.DROPDOWN_FONT_SIZE, "bold"),
            width=ComboConfig.HEIGHT * 5,
            height=ComboConfig.HEIGHT,
            variable=self.variable,
            state=state
        )
        combo.grid(column=0, row=1, columnspan=4, padx=40, pady=(10, 100))
        return combo
    
    def get_value(self) -> int:
        """Get the current value as integer"""
        return int(self.variable.get())
    
    def set_value(self, value: int):
        """Set the current value"""
        self.variable.set(str(value))
    
    def configure_combo(self, **kwargs):
        """Configure the combo box"""
        self.combo_box.configure(**kwargs)


class TotalPlayersWindow:
    """Main window for configuring total players and mafias"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.window = self._create_window()
        
        self._setup_title_frame()
        self.main_frame = self._setup_main_frame()
        self._setup_input_frames()
        self._setup_logic()
        self._setup_done_button()
    
    def _create_window(self) -> tk.Toplevel:
        """Create and configure the toplevel window"""
        window = tk.Toplevel(self.master)
        window.transient(self.master)
        window.grab_set()
        window.title("Total Players")
        window.config(bg=WindowConfig.BG_COLOR)
        utils.initialize_windows(window)
        return window
    
    def _setup_title_frame(self):
        """Setup the title frame"""
        TitleFrame(self.window, "windows/total_players/total_players.png")
    
    def _setup_main_frame(self) -> BackgroundFrame:
        """Setup the main content frame"""
        bg_frame = BackgroundFrame(
            self.window,
            "images/background_image.png",
            0, WindowConfig.TITLE_HEIGHT, 1, WindowConfig.MAIN_HEIGHT
        )
        return bg_frame
    
    def _setup_input_frames(self):
        """Setup player and mafia input frames"""
        player_range = [str(n) for n in range(4, 12)]
        
        self.player_frame = PlayerMafiaFrame(
            self.main_frame.frame,
            "PLAYERS",
            FrameConfig.REL_X,
            values=player_range,
            initial_value=str(utils.db.total_players),
            state="normal"
        )
        
        self.mafia_frame = PlayerMafiaFrame(
            self.main_frame.frame,
            "MAFIAS",
            FrameConfig.REL_X + 0.45,
            values=None,
            initial_value=str(utils.db.total_mafias),
            state="disabled"
        )
    
    def _setup_logic(self):
        """Setup the logic for enabling/disabling mafia input"""
        self._update_mafia_options()
        
        self.player_frame.configure_combo(command=lambda e: self._update_mafia_options())
        self.mafia_frame.configure_combo(command=lambda e: self._on_mafia_change())
    
    def _calculate_mafia_limit(self, player_num: int) -> int:
        """Calculate maximum number of mafias based on player count"""
        return (player_num // 2) if player_num % 2 == 0 else (player_num // 2 + 1)
    
    def _update_mafia_options(self):
        """Update mafia options based on player count"""
        player_num = self.player_frame.get_value()
        mafia_num = self.mafia_frame.get_value()
        
        # Update database with new player count
        utils.db.change_player_num(player_num)
        
        # Calculate mafia limit
        mafia_limit = self._calculate_mafia_limit(player_num)
        
        # Adjust mafia count if it exceeds limit
        if mafia_num >= mafia_limit:
            new_mafia_count = mafia_limit - 1
            self.mafia_frame.set_value(new_mafia_count)
            utils.db.change_mafia_num(new_mafia_count)
        
        # Update mafia combo box values
        mafia_values = [str(n) for n in range(1, mafia_limit)]
        
        # Enable/disable mafia input based on player count
        if player_num == 4:
            self.mafia_frame.configure_combo(values=mafia_values, state='disabled')
            self.mafia_frame.set_value(1)
        else:
            self.mafia_frame.configure_combo(values=mafia_values, state='normal')
    
    def _on_mafia_change(self):
        """Handle mafia count change"""
        mafia_num = self.mafia_frame.get_value()
        utils.db.change_mafia_num(mafia_num)
    
    def _setup_done_button(self):
        """Setup the done button"""
        normal = Image.open("windows/total_players/done_button/frame_1.png")
        pressed = Image.open("windows/total_players/done_button/frame_2.png")
        
        done_button = utils.Custom_Buttons(
            self.main_frame.frame,
            normal,
            pressed,
            bg="#0e0d0d",
            command=self._close_window
        )
        done_button.place(rely=0.83, relheight=0.15, relx=0.4, relwidth=0.15)
    
    def _close_window(self):
        """Close the window after a short delay"""
        self.window.after(100, self.window.destroy)


def create_window(master: tk.Tk):
    """
    Create a window for configuring total number of players.
    Entry point maintaining backward compatibility.
    """
    TotalPlayersWindow(master)