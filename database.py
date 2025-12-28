class Database:
    def __init__(self):
        self.total_players = 4
        self.total_mafias = 1
        self.players_left = 4
        self.mafias_left = 1
        self.players_list = []
        self.mafias_list = []
        self.sheriff = None
        self.doctor = None
        self.prompts = {}

    def change_player_num(self, player_num: int) -> None:
        self.total_players, self.players_left = player_num, player_num
        self.players_list = [(0, 0)] * player_num
    
    def change_mafia_num(self, mafia_num: int) -> None:
        self.total_mafias, self.mafias_left = mafia_num, mafia_num
        self.mafias_list = [0] * mafia_num