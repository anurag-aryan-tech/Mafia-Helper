import tkinter as tk
from utils import Utilities, util
from windows.total_players import total_player_window
from windows.roles import roles_window

utils = Utilities()

class Button_Commands:
    def __init__(self):
        pass

    def start_button_command(self, master):
        total_player_window.create_window(master)
    def roles_button_command(self, master):
        roles_window.create_window(master)