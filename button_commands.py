import tkinter as tk
from tkinter import messagebox
from utils import utils
from windows.total_players import total_player_window
from windows.roles import roles_window
from windows.prompts import prompts_window
from windows.night import night_window
from windows.day import day_window

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
            utils.nd_helper = utils.db.Night_Day_Helper()
            messagebox.showinfo("Reset", "All values have been reset successfully!")
    
    def prompts_button_command(self, master):
        if not utils.db.first_disable:
            messagebox.showwarning("Warning", "Set the Names and Roles of players to proceed!")
            return
        prompts_window.create_window(master)

    def night_button_command(self, master):
        if not utils.db.first_disable:
            messagebox.showwarning("Warning", "Set the Names and Roles of players to proceed!")
            return
        elif utils.nd_helper.night_number > utils.nd_helper.day_number:
            messagebox.showwarning("Warning", "Finish the current day before starting a new night!")
            return
        night_window.create_window(master)

    def day_button_command(self, master):
        if not utils.db.first_disable:
            messagebox.showwarning("Warning", "Set the Names and Roles of players to proceed!")
            return
        elif utils.nd_helper.day_number >= utils.nd_helper.night_number:
            messagebox.showwarning("Warning", "Finish the current night before starting a new day!")
            return
        day_window.create_window(master)

    
        