import tkinter as tk
from tkinter import messagebox
from utils import utils
from windows.total_players import total_player_window
from windows.roles import roles_window

class Button_Commands:
    def __init__(self):
        pass

    def start_button_command(self, master):
        if utils.db.first_disable:
            messagebox.showwarning("Warning", "Reset the window to change Player Number!")
            return
        total_player_window.create_window(master)
    def roles_button_command(self, master):
        if utils.db.first_disable:
            messagebox.showwarning("Warning", "Reset the window to change Names and Roles!")
            return
        roles_window.create_window(master)

    def reset_button_command(self):
        answer = messagebox.askyesno("Reset", "Are you sure you want to reset all values?")
        if answer:
            utils.db.reset_values()
            messagebox.showinfo("Reset", "All values have been reset successfully!")



        