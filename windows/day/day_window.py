import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from typing import Dict, List
from dataclasses import dataclass
from windows.prompts.prompts_window import ImageFrame

@dataclass
class DayWindowConfig:
    TITLE_IMAGE_PATH: str = "windows/day/day.png"
    BG_IMAGE_PATH: str = "images/background_image.png"

    TITLE_HEIGHT: int = 3
    BODY_HEIGHT: int = 10 - TITLE_HEIGHT

@dataclass
class StyleConfig:
    BG_COLOR: str = "#152e2e"

class DayPhaseWindow:
    def __init__(self, master: tk.Tk|tk.Toplevel) -> None:
        self.master = master
        self.window_config = DayWindowConfig()
        self.style_config = StyleConfig()
        self.window = self._create_window()

        self._setup_window_ui()

    def _setup_window_ui(self):
        self._create_frames()

    def _create_window(self):
        window = tk.Toplevel(self.master)
        window.title("Day Phase")
        window.config(bg=self.style_config.BG_COLOR)
        window.grab_set()
        window.transient(self.master)
        utils.initialize_windows(window)
        return window
    
    def _create_frames(self):
        title_height = self.window_config.TITLE_HEIGHT/10
        body_height = self.window_config.BODY_HEIGHT/10
        self.title_frame = ImageFrame(self.window, self.window_config.TITLE_IMAGE_PATH, 0, title_height)
        self.body_frame = ImageFrame(self.window, self.window_config.BG_IMAGE_PATH, title_height, body_height)

def create_window(master: tk.Tk | tk.Toplevel):
    DayPhaseWindow(master)