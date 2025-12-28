import tkinter
import customtkinter
from PIL import Image, ImageTk
from database import Database as db
class Utilities:
    def __init__(self) -> None:
        self.db = db()

    def zoom_control(self, window, event=None):
        '''
        Zoom in if the screen is not zoomed and vice-versa.
        '''
        zoomed = True if window.state() == "zoomed" else False
        if zoomed:
            window.state("normal")
        else:
            window.state("zoomed")

    def calculate_x_y(self, width: int, height: int, window):
        '''
        Calculate x and y position to center the window on the screen.
        '''
        window.update()
        x = (window.winfo_screenwidth() - width)//2
        y = (window.winfo_screenheight() - height)//2
        return x, y

    def hover_color(self, widget, on_enter: bool = True, color: str= "Black"):
        '''
        Changes color of the widget when the cursor Enter (hover) or Leave.
        Args:
            widget : tkinter widget created already
            on_enter : True means when entering; False means when leaving
            color : The color you want the widget to change to
        '''

        def color_change(widget, color: str):
            widget.config(bg=color)

        if on_enter:
            widget.bind("<Enter>", lambda event=None: color_change(widget, color))
        else:
            widget.bind("<Leave>", lambda event=None: color_change(widget, color))

    def photoimage_generator(self, path: str):
        '''
        Returns a photoimage based on the path of the image file.
        Args:
            path : the path of the image file
        '''
        image = Image.open(path)
        photoimage = ImageTk.PhotoImage(image)
        return photoimage

    def resize_image(self, path: str, width: int, height: int):
        image = Image.open(path)
        resized_image = image.resize((width, height))
        return ImageTk.PhotoImage(resized_image)
    
    def initialize_windows(self, window):

        # Calculate the position of the window at the center of the screen
        width, height = 1100, 650
        x, y = self.calculate_x_y(width, height, window)
        window.geometry(f"{width}x{height}+{x}+{y}")

        # Bind the ESC key to toggle the zoom state of the window
        window.bind("<Escape>", lambda event: self.zoom_control(window, event))

        # Create frames for the title and main content

        # Function to resize an image
    def image_config(self, event, label_name, last_size, img_path):
        # Only resize if dimensions actually changed
        if event.width != last_size['width'] or event.height != last_size['height']:
            last_size['width'] = event.width
            last_size['height'] = event.height

            image = self.resize_image(img_path, event.width, event.height)
            label_name.config(image=image)
            label_name.image = image  # Keep reference

    class Custom_Buttons:
        '''
        Create buttons with custom images when pressed or released.

        Args:
            master (tkinter.Widget): The master widget the button will be placed on.
            normal_image (PIL.Image.Image): The image to be displayed when not pressed.
            pressed_image (PIL.Image.Image): The image to be displayed when pressed.
            size (image size, optional): The size of the image to display. Defaults to None.
            command (function, optional): The function to be called when the button is pressed. Defaults to None.
        '''
        def __init__(self, master, normal_image, pressed_image, size=None, command=None, bg= None) -> None:
            if size:
                normal_image = normal_image.resize(size)
                pressed_image = pressed_image.resize(size)
            self.bg = bg if bg else "#2A332A"
            self.master = master
            self.normal_image = ImageTk.PhotoImage(normal_image)
            self.pressed_image = ImageTk.PhotoImage(pressed_image)
            self.command = command
            self.button = tkinter.Label(master, image=self.normal_image, borderwidth=0, bg=self.bg)
            self.button.bind("<Button-1>", self.on_press)
            self.button.bind("<ButtonRelease-1>", self.on_release)

        def on_release(self, event=None):
            self.button.config(image=self.normal_image)

        def on_press(self, event=None):
            self.button.config(image=self.pressed_image)
            if self.command:
                self.command()
            self.master.after(400, self.on_release)

        def pack(self, **kwargs):
            self.button.pack(kwargs)

        def pack(self, **kwargs):
            self.button.pack(kwargs)

        def grid(self, **kwargs):
            self.button.grid(kwargs)

        def place(self, **kwargs):
            self.button.place(kwargs)

        def winfo_reqwidth(self):
            self.button.update_idletasks()
            return self.button.winfo_reqwidth()

        def winfo_reqheight(self):
            self.button.update_idletasks()
            return self.button.winfo_reqheight()

util = Utilities()