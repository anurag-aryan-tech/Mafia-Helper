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
    CORNER_RADIUS: int = 15
    BORDER_WIDTH: int = 7

    FONT_FAMILY: str = "Garamond"
    TEXT_SIZE: int = 30
    TEXT_SIZE_SMALL: int = 20

    TOTAL_FRAMES: int = 3
    FRAME_RATIO: str = "0.25:0.6:0.15"
    FRAMES_RELY_RELHEIGHT: List[Tuple[float, float]] = field(default_factory=list)

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

        self._setup_window_ui()

    def _setup_window_ui(self):
        self._create_image_frames()
        self._setup_action_frames()

    def _setup_action_frames(self):
        self.phase_frame = PhaseFrame(self.body_frame)
        self.prompt_frame = PromptFrame(self.body_frame)
        self.footer_frame = FooterFrame(self.body_frame)

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

class FrameInteractions:
    def __init__(self):
        self.phase_var = tk.StringVar(value=f"Phase {utils.nd_helper.day_phase}")
        self.style_config = StyleConfig()
        self.rely_relheights = self.style_config.FRAMES_RELY_RELHEIGHT[:]

    def _create_frames(self, parent: tk.Frame|tk.Toplevel|ImageFrame, rely: float, relheight: float, relx: float = 0.0) -> tk.Frame:
        # Extract the actual frame if parent is ImageFrame
        actual_parent = parent.frame if isinstance(parent, ImageFrame) else parent
        
        frame = ctk.CTkFrame(
            actual_parent,
            fg_color=self.style_config.FG_COLOR,
            bg_color=self.style_config.BG_COLOR_FRAME,
            corner_radius=self.style_config.CORNER_RADIUS,
            border_width=self.style_config.BORDER_WIDTH,
            border_color=self.style_config.BD_COLOR
        )

        HoverEffects.apply_border_hover(
            frame, 
            self.style_config.HOVER_COLOR, 
            self.style_config.BD_COLOR
        )
        
        frame.place(relx=relx, rely=rely, relwidth=1-relx*2, relheight=relheight)
        return frame

class PhaseFrame(FrameInteractions):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame):
        super().__init__()
        self.parent = parent
        self.rely = self.rely_relheights[0][0]
        self.relheight = self.rely_relheights[0][1]

        self._setup_phase_frame()

    def _setup_phase_frame(self):
        self._create_phase_frame()

    def _create_phase_frame(self):
        self.phase_frame = self._create_frames(self.parent, self.rely, self.relheight)

class PromptFrame(FrameInteractions):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame):
        super().__init__()
        self.parent = parent
        self.rely = self.rely_relheights[1][0]
        self.relheight = self.rely_relheights[1][1]

        self._setup_prompt_frame()

    def _setup_prompt_frame(self):
        self._create_prompt_frame()

    def _create_prompt_frame(self):
        self.prompt_frame = self._create_frames(self.parent, self.rely, self.relheight)

class FooterFrame(FrameInteractions):
    def __init__(self, parent: tk.Frame|tk.Toplevel|ImageFrame):
        super().__init__()
        self.parent = parent
        self.rely = self.rely_relheights[2][0]
        self.relheight = self.rely_relheights[2][1]

        self._setup_footer_frame()

    def _setup_footer_frame(self):
        self._create_footer_frame()

    def _create_footer_frame(self):
        self.footer_frame = self._create_frames(self.parent, self.rely, self.relheight)

def create_window(master: tk.Tk | tk.Toplevel):
    DayPhaseWindow(master)