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
        self.prompts = all_prompts.all_prompts_dict

    def change_player_num(self, player_num: int) -> None:
        """Update total number of players"""
        self.total_players = player_num
        self.players_left = player_num
        self.players_list = [('', '')] * player_num
        self.change_msd(self.players_list)

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
            Get the player with most votes
            
            Returns:
                Tuple of (player_name, message) or (None, reason) if no clear winner
            """
            if not self.votes:
                return None, "No votes recorded"
            
            most_voted_player = max(self.votes, key=self.votes.get)  # type: ignore
            vote_count = self.votes[most_voted_player]
            total_votes = sum(self.votes.values())
            
            if vote_count > total_votes / 2:
                return most_voted_player, f"Got {vote_count} out of {total_votes} votes"
            return None, "No clear majority"

        def clear_votes(self) -> None:
            """Clear all votes"""
            self.votes = {}

        def set_doctor_save(self, player: str) -> None:
            """Set which player the doctor is saving"""
            self.doctor_save = player

        def investigate_result(self, player: str, database: 'Database') -> str:
            """
            Get sheriff investigation result for a player
            
            Returns:
                String describing if player is mafia or not
            """
            for name, role in database.players_list:
                if name.lower() == player.lower():
                    if role.lower() == 'mafia':
                        return f"{player.title()} is a Mafia."
                    return f"{player.title()} is not a Mafia."
            return "Player not found"
            
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