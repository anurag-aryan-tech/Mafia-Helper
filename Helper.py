from typing import Dict, Tuple, Optional, Callable
import tkinter as tk
import customtkinter as ctk
from button_commands import Button_Commands
from utils import utils
from PIL import Image, ImageTk
from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Main window configuration"""
    TITLE = "MAIN PAGE"
    BG_COLOR = "#0E0D0B"
    MIN_WIDTH = 600
    MIN_HEIGHT = 450
    WIDTH = 800
    HEIGHT = 550


@dataclass
class FrameConfig:
    """Frame styling configuration"""
    FRAME_COLOR = "#2A332A"
    CORNER_RADIUS = 45
    PADDING = 5


@dataclass
class ButtonPlacement:
    """Button placement configuration"""
    REL_WIDTH = 0.6
    REL_HEIGHT = 0.6
    REL_X = 0.2
    REL_Y = 0.2


class ImageLabel:
    """Manages a label with a dynamically resizing image"""
    
    def __init__(self, parent: tk.Widget, image_path: str):
        self.parent = parent
        self.image_path = image_path
        self.label = tk.Label(parent)
        self.last_size = {'width': 0, 'height': 0}
        self.current_image = None  # Store reference to prevent garbage collection
        
        self._setup()
    
    def _setup(self):
        """Setup the label and bind resize event"""
        self.label.place(relwidth=1, relheight=1, relx=0, rely=0)
        self.label.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        """Handle resize event"""
        if event.width != self.last_size['width'] or event.height != self.last_size['height']:
            self.last_size['width'] = event.width
            self.last_size['height'] = event.height
            
            self.current_image = utils.resize_image(self.image_path, event.width, event.height)
            self.label.config(image=self.current_image)


class MainFrame:
    """Manages the main content frame with buttons"""
    
    def __init__(self, parent, button_commands: Button_Commands):
        self.parent = parent
        self.button_commands = button_commands
        self.frame: tk.Frame
        self.button_frames: Dict[str, ctk.CTkFrame] = {}
        self.buttons = {}
        self.bg_image = None  # Store reference to prevent garbage collection
        
        self._create_frame()
        self._setup_grid()
        self._create_background()
        self._create_button_frames()
        self._create_buttons()
    
    def _create_frame(self):
        """Create the main frame"""
        self.frame = tk.Frame(self.parent, bd=1, bg=WindowConfig.BG_COLOR)
        self.frame.place(relheight=0.75, relwidth=1, relx=0, rely=0.225)
    
    def _setup_grid(self):
        """Configure grid layout"""
        total_columns = 5
        total_rows = 5
        
        for col in range(total_columns):
            self.frame.columnconfigure(col, weight=1, uniform="column_group")
        for row in range(total_rows):
            self.frame.rowconfigure(row, weight=1, uniform="row_group")
    
    def _create_background(self):
        """Create background image"""
        self.bg_image = ImageTk.PhotoImage(
            Image.open("images/background_image.png").resize((1360, 600))
        )
        background_label = tk.Label(self.frame, image=self.bg_image)
        background_label.grid(row=0, column=0, rowspan=5, columnspan=5)
    
    def _create_button_frames(self):
        """Create frames for holding buttons"""
        frame_specs = [
            ("start", 2, 0, None, (FrameConfig.PADDING + 3, 0)),
            ("roles", 1, 2, None, None),
            ("prompts", 3, 2, None, None),
            ("night", 0, 4, (10, 0), (0, FrameConfig.PADDING)),
            ("day", 4, 4, (0, 10), (FrameConfig.PADDING, 0)),
            ("reset", 2, 4, None, (0, FrameConfig.PADDING))
        ]
        
        for name, column, row, padx, pady in frame_specs:
            frame = ctk.CTkFrame(
                self.frame,
                fg_color=FrameConfig.FRAME_COLOR,
                corner_radius=FrameConfig.CORNER_RADIUS
            )
            frame.grid(column=column, row=row, sticky="nsew", padx=padx, pady=pady)
            self.button_frames[f"{name}_button_frame"] = frame
    
    def _create_buttons(self):
        """Create all buttons"""
        button_specs = [
            ("start", (82, 65), lambda: self.button_commands.start_button_command(self._get_root())),
            ("roles", (86, 48), lambda: self.button_commands.roles_button_command(self._get_root())),
            ("prompts", (97, 85), lambda: self.button_commands.prompts_button_command(self._get_root())),
            ("night", (97, 85), lambda: self.button_commands.night_button_command(self._get_root())),
            ("day", (97, 85), lambda: self.button_commands.day_button_command(self._get_root())),
            ("reset", (85, 75), lambda: self.button_commands.reset_button_command())
        ]
        
        for name, size, command in button_specs:
            btn_name = f"{name}_button"
            frame = self.button_frames[f"{btn_name}_frame"]
            
            image_1 = Image.open(f"{btn_name}/frame_1.png")
            image_2 = Image.open(f"{btn_name}/frame_2.png")
            
            button = utils.Custom_Buttons(frame, image_1, image_2, size, command)
            button.place(
                relx=ButtonPlacement.REL_X,
                rely=ButtonPlacement.REL_Y,
                relwidth=ButtonPlacement.REL_WIDTH,
                relheight=ButtonPlacement.REL_HEIGHT
            )
            self.buttons[btn_name] = button
    
    def _get_root(self):
        """Get the root Tk window"""
        widget = self.parent
        while widget.master is not None:
            widget = widget.master
        return widget


class MainApplication:
    """Main application controller"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.button_commands = Button_Commands()
        
        self._setup_window()
        self._create_title_frame()
        self._create_main_frame()
    
    def _setup_window(self):
        """Configure the main window"""
        self.root.title(WindowConfig.TITLE)
        self.root.config(bg=WindowConfig.BG_COLOR)
        self.root.minsize(WindowConfig.MIN_WIDTH, WindowConfig.MIN_HEIGHT)
        
        # Center window
        x, y = utils.calculate_x_y(
            WindowConfig.WIDTH,
            WindowConfig.HEIGHT,
            self.root
        )
        self.root.geometry(f"{WindowConfig.WIDTH}x{WindowConfig.HEIGHT}+{x}+{y}")
        
        # Bind ESC for zoom control
        self.root.bind("<Escape>", lambda event: utils.zoom_control(self.root, event))
    
    def _create_title_frame(self):
        """Create the title frame with image"""
        title_frame = tk.Frame(
            self.root,
            bd=3,
            relief="ridge",
            bg=WindowConfig.BG_COLOR,
            highlightbackground=WindowConfig.BG_COLOR
        )
        title_frame.place(relheight=0.225, relwidth=1, relx=0, rely=0)
        
        # Create image label
        ImageLabel(title_frame, "images/title_image.png")
    
    def _create_main_frame(self):
        """Create the main content frame"""
        MainFrame(self.root, self.button_commands)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Application entry point"""
    app = MainApplication()
    app.run()


if __name__ == "__main__":
    main()