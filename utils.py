"""
utils.py - Refactored with subtle improvements
"""
import tkinter as tk
from PIL import Image, ImageTk
from typing import Tuple, Optional, Callable
from database import Database


class Utilities:
    """Utility functions for window management and UI helpers"""
    
    def __init__(self) -> None:
        self.db = Database()
        self.nd_helper = self.db.Night_Day_Helper()

    def zoom_control(self, window: tk.Tk, event: Optional[tk.Event] = None) -> None:
        """Toggle window between zoomed and normal state"""
        zoomed = window.state() == "zoomed"
        window.state("normal" if zoomed else "zoomed")

    def calculate_x_y(self, width: int, height: int, window: tk.Tk|tk.Toplevel) -> Tuple[int, int]:
        """Calculate x and y position to center the window on screen"""
        window.update()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        return x, y

    def hover_color(self, widget, on_enter: bool = True, color: str = "Black") -> None:
        """
        Change widget color on mouse hover/leave
        
        Args:
            widget: The tkinter widget to apply hover effect to
            on_enter: True for enter event, False for leave event
            color: The color to change to
        """
        event_type = "<Enter>" if on_enter else "<Leave>"
        widget.bind(event_type, lambda e: widget.config(bg=color))

    def photoimage_generator(self, path: str) -> ImageTk.PhotoImage:
        """Generate PhotoImage from file path"""
        return ImageTk.PhotoImage(Image.open(path))

    def resize_image(self, path: str, width: int, height: int) -> ImageTk.PhotoImage:
        """Resize image and return as PhotoImage"""
        image = Image.open(path).resize((width, height))
        return ImageTk.PhotoImage(image)
    
    def initialize_windows(self, window) -> None:
        """Initialize window with default size, position, and key bindings"""
        width, height = 1100, 650
        x, y = self.calculate_x_y(width, height, window)
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.bind("<Escape>", lambda event: self.zoom_control(window, event))

    def image_config(self, event: tk.Event, label: tk.Label, 
                    last_size: dict, img_path: str) -> None:
        """Handle image resize on window configure event"""
        if event.width != last_size['width'] or event.height != last_size['height']:
            last_size['width'] = event.width
            last_size['height'] = event.height
            image = self.resize_image(img_path, event.width, event.height)
            label.config(image=image)
            label.image = image  # type: ignore  # Keep reference to prevent garbage collection

    class Custom_Buttons:
        """
        Custom button widget with image states for pressed/released
        
        Args:
            master: Parent widget
            normal_image: Image when button is not pressed
            pressed_image: Image when button is pressed
            size: Optional tuple for image dimensions
            command: Optional callback function
            bg: Optional background color
        """
        
        def __init__(self, master: tk.Widget, normal_image: Image.Image, 
                    pressed_image: Image.Image, size: Optional[Tuple[int, int]] = None,
                    command: Optional[Callable] = None, bg: Optional[str] = None) -> None:
            if size:
                normal_image = normal_image.resize(size)
                pressed_image = pressed_image.resize(size)
            
            self.bg = bg or "#2A332A"
            self.master = master
            self.normal_image = ImageTk.PhotoImage(normal_image)
            self.pressed_image = ImageTk.PhotoImage(pressed_image)
            self.command = command
            
            self.button = tk.Label(master, image=self.normal_image, borderwidth=0, bg=self.bg)
            self.button.bind("<Button-1>", self.on_press)
            self.button.bind("<ButtonRelease-1>", self.on_release)

        def on_release(self, event: Optional[tk.Event] = None) -> None:
            """Reset button to normal image"""
            self.button.config(image=self.normal_image)

        def on_press(self, event: Optional[tk.Event] = None) -> None:
            """Handle button press - change image and execute command"""
            self.button.config(image=self.pressed_image)
            if self.command:
                self.command()
            self.master.after(400, self.on_release)

        def pack(self, **kwargs) -> None:
            """Pack the button widget"""
            self.button.pack(**kwargs)

        def grid(self, **kwargs) -> None:
            """Grid the button widget"""
            self.button.grid(**kwargs)

        def place(self, **kwargs) -> None:
            """Place the button widget"""
            self.button.place(**kwargs)

        def winfo_reqwidth(self) -> int:
            """Get required width of button"""
            self.button.update_idletasks()
            return self.button.winfo_reqwidth()

        def winfo_reqheight(self) -> int:
            """Get required height of button"""
            self.button.update_idletasks()
            return self.button.winfo_reqheight()


# Global instance for backward compatibility
utils = Utilities()