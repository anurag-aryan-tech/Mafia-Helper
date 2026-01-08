import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from utils import utils
from PIL import Image
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Window layout configuration"""
    BG_COLOR = "#152e2e"
    TITLE_HEIGHT = 0.2
    BODY_HEIGHT = 0.7
    FOOTER_HEIGHT = 0.1
    FOOTER_Y = 0.9


@dataclass
class StyleConfig:
    """Styling configuration"""
    FG_COLOR = "#0B0F14"
    BD_COLOR = "#3A3F45"
    HOVER_COLOR = "#FF2A2A"
    FOOTER_COLOR = "#171717"
    LABEL_COLOR = "#8392a3"
    TEXT_COLOR = "#E6EAF0"
    SUBLABEL_COLOR = "#545c66"
    
    CORNER_RADIUS = 15
    BORDER_WIDTH = 7
    COMBO_BORDER_WIDTH = 5
    ENTRY_BORDER_WIDTH = 5


class ImageFrame:
    """Frame with dynamically resizing background image"""
    
    def __init__(self, parent, image_path: str, 
                 rely: float, relheight: float):
        self.parent = parent
        self.image_path = image_path
        self.last_size = {"width": 0, "height": 0}
        
        self.frame = tk.Frame(parent)
        self.frame.place(relx=0, rely=rely, relwidth=1, relheight=relheight)
        
        self.label = tk.Label(self.frame)
        self.label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.label.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        """Handle resize event"""
        utils.image_config(event, self.label, self.last_size, self.image_path)


class PlayerCard:
    """Individual player card with name and role inputs"""
    
    def __init__(self, parent: tk.Frame, position: int, 
                 available_roles: List[str], style: StyleConfig):
        self.parent = parent
        self.position = position
        self.style = style
        
        # Get existing player data
        player_data = utils.db.players_list[position]
        self.name_var = tk.StringVar(value=player_data[0])
        self.role_var = tk.StringVar(value=player_data[1].title())
        
        self.frame = self._create_frame()
        self._create_widgets(available_roles)
    
    def _create_frame(self) -> ctk.CTkFrame:
        """Create the card frame"""
        frame = ctk.CTkFrame(
            self.parent,
            bg_color=StyleConfig.FOOTER_COLOR,
            fg_color=self.style.FG_COLOR,
            border_width=self.style.BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            corner_radius=self.style.CORNER_RADIUS
        )
        return frame
    
    def _create_widgets(self, available_roles: List[str]):
        """Create all widgets in the card"""
        # Title label
        title = ctk.CTkLabel(
            self.frame,
            text=f"Speaker {self.position + 1}",
            font=ctk.CTkFont("Garamond", 35, 'bold'),
            bg_color='transparent',
            fg_color='transparent',
            text_color=self.style.LABEL_COLOR
        )
        title.place(relx=0.05, rely=0.1, relheight=0.2, relwidth=0.9)
        
        # Name section
        name_label = ctk.CTkLabel(
            self.frame,
            text="NAME : ",
            fg_color='transparent',
            text_color=self.style.SUBLABEL_COLOR,
            font=ctk.CTkFont("Garamond", 17, 'bold')
        )
        name_label.place(relx=0.05, relwidth=0.2, rely=0.4, relheight=0.2)
        
        self.name_entry = ctk.CTkEntry(
            self.frame,
            corner_radius=7,
            border_width=self.style.ENTRY_BORDER_WIDTH,
            border_color=self.style.BD_COLOR,
            fg_color=self.style.FG_COLOR,
            bg_color="transparent",
            text_color=self.style.TEXT_COLOR,
            font=("Garamond", 18, 'bold'),
            justify='center',
            textvariable=self.name_var
        )
        self.name_entry.place(relx=0.3, relwidth=0.6, rely=0.4, relheight=0.2)
        
        # Role section
        role_label = ctk.CTkLabel(
            self.frame,
            text="ROLE : ",
            fg_color='transparent',
            text_color=self.style.SUBLABEL_COLOR,
            font=ctk.CTkFont("Garamond", 17, 'bold')
        )
        role_label.place(relx=0.05, relwidth=0.2, rely=0.7, relheight=0.2)
        
        self.role_combo = ctk.CTkComboBox(
            self.frame,
            corner_radius=self.style.CORNER_RADIUS,
            border_width=self.style.COMBO_BORDER_WIDTH,
            bg_color="transparent",
            font=("Garamond", 22, "bold"),
            text_color=self.style.TEXT_COLOR,
            fg_color=self.style.FG_COLOR,
            border_color=self.style.BD_COLOR,
            button_color=self.style.BD_COLOR,
            button_hover_color=self.style.HOVER_COLOR,
            dropdown_fg_color=self.style.FG_COLOR,
            dropdown_text_color=self.style.TEXT_COLOR,
            dropdown_font=("Garamond", 18, "bold"),
            variable=self.role_var,
            values=available_roles
        )
        self.role_combo.place(relx=0.3, relwidth=0.6, rely=0.7, relheight=0.2)
        
        # Apply hover effects
        self._apply_hover_effects()
    
    def _apply_hover_effects(self):
        """Apply hover effects to interactive elements"""
        def on_enter(widget):
            widget.configure(border_color=self.style.HOVER_COLOR)
        
        def on_exit(widget):
            widget.configure(border_color=self.style.BD_COLOR)
        
        for widget in [self.frame, self.name_entry, self.role_combo]:
            widget.bind("<Enter>", lambda e, w=widget: on_enter(w))
            widget.bind("<Leave>", lambda e, w=widget: on_exit(w))
    
    def grid(self, row: int, column: int):
        """Grid the card frame"""
        self.frame.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)
    
    def get_name(self) -> str:
        """Get current name value"""
        return self.name_var.get()
    
    def get_role(self) -> str:
        """Get current role value"""
        return self.role_var.get()
    
    def set_role_values(self, values: List[str]):
        """Update available role values"""
        self.role_combo.configure(values=values)
    
    def reset_role(self):
        """Reset role to empty"""
        self.role_var.set("")


class RoleManager:
    """Manages role availability and validation"""
    
    def __init__(self, total_players: int, total_mafias: int):
        self.total_players = total_players
        self.total_mafias = total_mafias
        self.villager_count = total_players - total_mafias - 2  # -2 for sheriff and doctor
    
    def get_available_roles(self) -> List[str]:
        """Get list of currently available roles"""
        role_count = self._count_roles()
        
        available = [""]
        if role_count['villager'] < self.villager_count:
            available.append("Villager")
        if role_count['mafia'] < self.total_mafias:
            available.append("Mafia")
        if role_count['sheriff'] == 0:
            available.append("Sheriff")
        if role_count['doctor'] == 0:
            available.append("Doctor")
        
        return available
    
    def _count_roles(self) -> Dict[str, int]:
        """Count how many of each role are assigned"""
        role_count = {
            "": 0,
            "villager": 0,
            "mafia": 0,
            "sheriff": 0,
            "doctor": 0,
        }
        for _, role in utils.db.players_list:
            role_count[role] += 1
        return role_count


class RolesWindow:
    """Main window for assigning player names and roles"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.window = self._create_window()
        self.style = StyleConfig()
        
        self.role_manager = RoleManager(utils.db.total_players, utils.db.total_mafias)
        self.player_cards: List[PlayerCard] = []
        
        self._setup_frames()
        self._create_player_cards()
        self._setup_done_button()
    
    def _create_window(self) -> tk.Toplevel:
        """Create and configure the toplevel window"""
        window = tk.Toplevel(self.master)
        window.transient(self.master)
        window.grab_set()
        window.title("Roles")
        window.config(bg=WindowConfig.BG_COLOR)
        utils.initialize_windows(window)
        return window
    
    def _setup_frames(self):
        """Setup title, body, and footer frames"""
        # Title frame
        ImageFrame(
            self.window,
            "windows/roles/roles.png",
            0,
            WindowConfig.TITLE_HEIGHT
        )
        
        # Body frame
        body_image_frame = ImageFrame(
            self.window,
            "images/background_image.png",
            WindowConfig.TITLE_HEIGHT,
            WindowConfig.BODY_HEIGHT
        )
        self.body_frame = body_image_frame.frame
        
        # Footer frame
        self.footer_frame = ctk.CTkFrame(
            self.window,
            fg_color=StyleConfig.FOOTER_COLOR
        )
        self.footer_frame.place(
            relx=0,
            rely=WindowConfig.FOOTER_Y,
            relwidth=1,
            relheight=WindowConfig.FOOTER_HEIGHT
        )
    
    def _create_player_cards(self):
        """Create player cards in grid layout"""
        player_count = utils.db.total_players
        rows = (player_count + 2) // 3
        columns = 3
        
        # Configure grid
        for row in range(rows):
            self.body_frame.rowconfigure(row, weight=1)
        for column in range(columns):
            self.body_frame.columnconfigure(column, weight=1)
        
        # Create cards
        available_roles = self.role_manager.get_available_roles()
        position = 0
        
        for row in range(rows):
            for col in range(columns):
                if position < player_count:
                    card = PlayerCard(
                        self.body_frame,
                        position,
                        available_roles,
                        self.style
                    )
                    card.grid(row, col)
                    
                    # Bind events
                    self._bind_card_events(card, position)
                    
                    self.player_cards.append(card)
                    position += 1
    
    def _bind_card_events(self, card: PlayerCard, position: int):
        """Bind events for name and role changes"""
        # Name change event
        def on_name_change(event=None):
            utils.db.change_player_name(card.get_name(), position + 1)
        
        card.name_entry.bind("<FocusOut>", on_name_change)
        
        # Role change event
        def on_role_change(selected_role: str):
            try:
                utils.db.change_players_list(
                    card.get_name(),
                    selected_role.lower(),
                    position + 1
                )
                self._update_all_role_options()
            except Exception as e:
                print(f"Error updating role: {e}")
                messagebox.showerror("Error", f"Failed to update role: {e}")
                card.reset_role()
        
        card.role_combo.configure(command=on_role_change)
    
    def _update_all_role_options(self):
        """Update available roles for all player cards"""
        available_roles = self.role_manager.get_available_roles()
        for card in self.player_cards:
            card.set_role_values(available_roles)
    
    def _setup_done_button(self):
        """Setup the done button"""
        normal = Image.open("windows/total_players/done_button/frame_1.png")
        pressed = Image.open("windows/total_players/done_button/frame_2.png")
        
        done_button = utils.Custom_Buttons(
            self.footer_frame,
            normal,
            pressed,
            bg=StyleConfig.FOOTER_COLOR,
            command=self._on_done
        )
        done_button.place(rely=0.05, relheight=0.9, relx=0.3, relwidth=0.4)
    
    def _on_done(self):
        """Handle done button click"""
        def done_command():
            self.window.focus_set()
            self.window.update_idletasks()
            
            # Validate all names and roles are filled
            for name, role in utils.db.players_list:
                if not name or not role:
                    messagebox.showwarning(
                        "Missing Values",
                        "Some 'Names' and/or 'Roles' are missing!!"
                    )
                    return
            
            # Confirm action
            answer = messagebox.askokcancel(
                "Proceed",
                "Action cannot be undone! If proceeded, you cannot change "
                "names, roles and numbers of players!"
            )
            if answer:
                utils.db.change_first_disable()
                self.window.destroy()
        
        self.window.after(100, done_command)


def create_window(master: tk.Tk):
    """
    Create a window for assigning roles to players.
    Entry point maintaining backward compatibility.
    """
    RolesWindow(master)