import tkinter as tk
import customtkinter as ctk
from button_commands import Button_Commands
from utils import utils
from PIL import Image, ImageTk

# ========================================MAIN PAGE========================================
main = tk.Tk()
main.title("MAIN PAGE")
main.config(bg="#0E0D0B")
main.minsize(600, 450)

button_commands = Button_Commands()

# Placing the window at the centre initially
width = 800
height = 550
x, y = utils.calculate_x_y(width, height, main)
main.geometry(f"{width}x{height}+{x}+{y}")

# Use ESC key to maximize or minimize
main.bind("<Escape>", lambda event: utils.zoom_control(main, event))

# ===================================CREATING FRAMES===================================

# 1. Title Frame: To display the title of the window.
img_path = "images/title_image.png"
title_frame = tk.Frame(main, bd= 3, relief="ridge", bg="#0E0D0B", highlightbackground="#0E0D0B")
title_frame.place(relheight=0.225, relwidth=1, relx=0, rely=0)

# Store previous dimensions
last_size_1 = {'width': 0, 'height': 0}

def image_config(event, label_name, last_size, img_path):
    # Only resize if dimensions actually changed
    if event.width != last_size['width'] or event.height != last_size['height']:
        last_size['width'] = event.width
        last_size['height'] = event.height
        
        image = utils.resize_image(img_path, event.width, event.height)
        label_name.config(image=image)
        label_name.image = image  # Keep reference

title_label = tk.Label(title_frame)
title_label.place(relwidth=1, relheight=1, relx=0, rely=0)
title_label.bind("<Configure>", lambda event: image_config(event, title_label, last_size_1, img_path))


# 2. Main Frame: Contains all the buttons for other windows
main_frame = tk.Frame(main, bd=1, bg="#0E0D0B")
main_frame.place(relheight=0.75, relwidth=1, relx=0, rely=0.225)



# - Dividing the frame into rows and columns
total_columns = 5
total_rows = 5
for col in range(total_columns):
    main_frame.columnconfigure(col, weight=1, uniform="column_group")
for row in range(total_rows):
    main_frame.rowconfigure(row, weight=1, uniform="row_group")

last_size_2 = {'width': 0, 'height': 0}
bg_image = ImageTk.PhotoImage(Image.open("images/background_image.png").resize((1360, 600)))
background_label = tk.Label(main_frame)
background_label.grid(row=0, column=0, rowspan=5, columnspan=5)
background_label.config(image=bg_image)

# - Creating frames for holding the buttons
frame_color = "#2A332A"
pady = 5
corner = 45

frame_attr = [("start", 2, 0, None, (pady+3, 0)),
            ("roles", 1, 2, None, None),
            ("prompts", 3, 2, None, None),
            ("night", 0, 4, (10, 0), (0, pady)),
            ("day", 4, 4, (0, 10), (pady, 0)),
            ("reset", 2, 4, None, (0, pady))]

for name, column, row, padx, pady in frame_attr:
    frame = globals()[f"{name}_button_frame"] = ctk.CTkFrame(main_frame, fg_color=frame_color, corner_radius=corner)
    frame.grid(column=column, row=row, sticky="nsew", padx = padx, pady=pady)

# - Creating the actual buttons

rel_width, rel_height = 0.6, 0.6
rel_x, rel_y = 0.2, 0.2

button_attr = [("start", (82, 65), lambda event=None: button_commands.start_button_command(main)),
            ("roles", (86, 48), lambda event=None: button_commands.roles_button_command(main)),
            ("prompts", (97, 85), lambda event=None: button_commands.prompts_button_command(main)),
            ("night", (97, 85), lambda event=None: button_commands.night_button_command(main)),
            ("day", (97, 85), None),
            ("reset", (85, 75), lambda event=None: button_commands.reset_button_command())]

main_buttons = {}

for name, size, command in button_attr:
    btn_name = f"{name}_button"
    frame = globals()[f"{btn_name}_frame"]
    image_1, image_2 = Image.open(f"{btn_name}/frame_1.png"), Image.open(f"{btn_name}/frame_2.png")

    main_buttons[btn_name] = utils.Custom_Buttons(frame, image_1, image_2, size, command)
    main_buttons[btn_name].place(relx=rel_x, rely= rel_y, relwidth= rel_width, relheight=rel_height)

main.mainloop()