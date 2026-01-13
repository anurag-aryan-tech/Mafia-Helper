from tkinter import messagebox
import windows.prompts.all_prompts as all_prompts
from typing import List, Tuple, Optional


class Database:
    """Main database for storing game state and player information"""
    
    def __init__(self):
        self.total_players: int = 4
        self.total_mafias: int = 1
        self.players_left: int = 4
        self.mafias_left: int = 1
        self.players_list: List[Tuple[str, str]] = [('', '')] * self.total_players
        self.mafias_list: List[str] = []
        self.sheriff: Optional[str] = None
        self.doctor: Optional[str] = None
        self.first_disable: bool = False
        self.eliminated_players: List[str] = []
        self.prompts = all_prompts.all_prompts_dict

    def change_player_num(self, player_num: int) -> None:
        """Update total number of players"""
        self.total_players = player_num
        self.players_left = player_num
        self.players_list = [('', '')] * player_num
        self.change_msd(self.players_list)

    def calculate_left(self) -> None:
        self.players_left = 0
        self.mafias_left = 0
        for _, role in self.players_list:
            if role.lower() == "mafia":
                self.mafias_left += 1
            else:
                self.players_left += 1
        self.change_msd(self.players_list)

    def check_win(self) -> dict[str, bool]:
        result = {
            "town_win" : False,
            "mafia_win" : False
        }
        if self.mafias_left <= 0:
            result["town_win"] = True
        elif self.players_left <= self.mafias_left:
            result["mafia_win"] = True

        return result

    def change_mafia_num(self, num: int) -> None:
        """Update total number of mafias"""
        self.total_mafias = num

    def player_num_checker(self, lst: List[Tuple[str, str]]) -> List[bool]:
        """
        Validate player role assignments
        
        Returns:
            List of booleans indicating if each constraint is satisfied:
            [mafia_count_valid, sheriff_count_valid, doctor_count_valid, enough_slots]
        """
        mafia_count = sum(1 for _, role in lst if role.lower() == 'mafia')
        sheriff_count = sum(1 for _, role in lst if role.lower() == 'sheriff')
        doctor_count = sum(1 for _, role in lst if role.lower() == 'doctor')
        remaining_slots = sum(1 for _, role in lst if role == '')
        
        mafia_left = self.total_mafias - mafia_count
        sheriff_left = 1 - sheriff_count
        doctor_left = 1 - doctor_count
        
        return [
            mafia_left >= 0,
            sheriff_left >= 0,
            doctor_left >= 0,
            mafia_left + sheriff_left + doctor_left <= remaining_slots
        ]

    def change_players_list(self, name: str, role: str, position: int) -> None:
        """
        Update player at given position
        
        Raises:
            ValueError: If position is invalid or role assignment violates constraints
        """
        if not (1 <= position <= self.total_players):
            raise ValueError("Invalid Position!")
        
        test_list = self.players_list[:]
        test_list[position - 1] = (name, role)
        result = self.player_num_checker(test_list)
        
        if not all(result):
            error_msgs = []
            if not result[0]:
                error_msgs.append(f"Too many mafias (max: {self.total_mafias})")
            if not result[1]:
                error_msgs.append("Sheriff already assigned")
            if not result[2]:
                error_msgs.append("Doctor already assigned")
            if not result[3]:
                error_msgs.append("Not enough remaining slots for required roles")
            raise ValueError(", ".join(error_msgs))
        
        self.players_list[position - 1] = (name, role)
        self.change_msd(self.players_list)

    def change_msd(self, player_list: List[Tuple[str, str]]) -> None:
        """Update mafias list, sheriff, and doctor based on player list"""
        self.mafias_list = []
        self.sheriff = None
        self.doctor = None
        
        for name, role in player_list:
            role_lower = role.lower()
            if role_lower == 'mafia':
                self.mafias_list.append(name)
            elif role_lower == 'sheriff':
                self.sheriff = name
            elif role_lower == 'doctor':
                self.doctor = name
    
    def change_player_name(self, name: str, position: int) -> None:
        """Update player name at given position without changing role"""
        if not (1 <= position <= self.total_players):
            raise ValueError("Invalid Position!")
        
        _, role = self.players_list[position - 1]
        self.players_list[position - 1] = (name, role)
        self.change_msd(self.players_list)
        
    def change_first_disable(self) -> None:
        """Toggle first_disable flag"""
        self.first_disable = not self.first_disable

    def reset_values(self) -> None:
        """Reset all database values to defaults"""
        self.__init__()

    class Night_Day_Helper:
        """Helper class for managing night and day phase data"""
        
        def __init__(self):
            self.night_number: int = 1
            self.day_number: int = 1
            self.night_phase: int = 1
            self.day_phase: int = 1
            self.dialogues: dict[str, str] = {}
            self.votes: dict[str, int] = {}
            self.doctor_save: Optional[str] = None
            self.day_message: str = ""
            self.eliminated_this_night: Optional[str] = None
            
        def add_dialogue(self, speaker: str, message: str) -> None:
            """Record dialogue from a speaker"""
            self.dialogues[speaker] = message

        def get_dialogues(self) -> str:
            """Get formatted string of all dialogues"""
            if not self.dialogues:
                return "None"
            
            lines = [f"{i + 1}. {speaker.title()}: {message}" 
                    for i, (speaker, message) in enumerate(self.dialogues.items())]
            return "\n".join(lines)

        def clear_dialogues(self) -> None:
            """Clear all dialogues"""
            self.dialogues = {}

        def add_vote(self, votee: str) -> None:
            """Add a vote for a player"""
            votee_lower = votee.lower()
            self.votes[votee_lower] = self.votes.get(votee_lower, 0) + 1

        def most_voted(self) -> Tuple[Optional[str], str]:
            """
            Get the player with most votes, considering doctor save.
            Prevents multiple eliminations in the same night.
            
            Returns:
                Tuple of (player_name, message) or (None, reason) if no clear winner
            """
            if not self.votes:
                return None, "No votes recorded"
            
            # Check if someone was already eliminated this night
            if self.eliminated_this_night:
                return None, f"A player has already been eliminated this night ({self.eliminated_this_night.title()})."
            
            # Sort players by vote count (descending) and then alphabetically for consistency
            sorted_votes = sorted(self.votes.items(), key=lambda x: (-x[1], x[0]))
            most_voted_player, vote_count = sorted_votes[0]
            total_votes = sum(self.votes.values())
            
            # Check if the doctor saved the most-voted player
            if self.doctor_save and most_voted_player.lower() == self.doctor_save.lower():
                if len(sorted_votes) > 1:
                    # If there is another player with votes, consider them next
                    next_player, next_vote_count = sorted_votes[1]
                    self.eliminated_this_night = next_player
                    return next_player, f"{next_player.title()} was eliminated with {next_vote_count} votes (doctor saved {most_voted_player.title()})."
                return None, f"No elimination (doctor saved {most_voted_player.title()})."
            
            # If votes exist, the most-voted player is eliminated (handles single mafia case)
            self.eliminated_this_night = most_voted_player
            return most_voted_player, f"{most_voted_player.title()} was eliminated with {vote_count} out of {total_votes} votes."

        def clear_votes(self) -> None:
            """Clear all votes"""
            self.votes = {}

        def reset_night_state(self) -> None:
            """Reset night elimination tracking for a new night"""
            self.eliminated_this_night = None

        def increment_night(self) -> None:
            """Increment night number for the next night phase"""
            self.night_number += 1
            self.night_phase = 1
            self.day_phase = 1
            self.eliminated_this_night = None

        def increment_day(self) -> None:
            """Increment day number for the next day phase"""
            self.day_number += 1
            self.day_phase = 1
            self.night_phase = 1

        def set_doctor_save(self, player: str) -> None:
            """Set which player the doctor is saving"""
            self.doctor_save = player

        def investigate_result(self, player: str, database: 'Database') -> str:
            result = "Player not found"
            for name, role in database.players_list:
                if name.lower() == player.lower():
                    if role.lower() == 'mafia':
                        result = f"{player.title()} is a Mafia."
                    else:
                        result = f"{player.title()} is not a Mafia."
                    break  # stop once found
            messagebox.showinfo(
                "Sheriff Investigation",
                f"Investigated {player.title()}: {result}\nCopy Sheriff prompt to clipboard."
            )
            return result

            
        def check_died(self, target: str) -> bool:
            """Check if target died (returns False if doctor saved them)"""
            if self.doctor_save and target.lower() == self.doctor_save.lower():
                return False
            return True

        def change_day_message(self, died_player: str) -> None:
            """Update the day message with elimination result"""
            self.day_message = (
                f"## Night {self.night_number} ended.\n"
                f"{died_player.title()} was eliminated during the night."
            )