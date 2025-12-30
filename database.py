class Database:
    def __init__(self):
        self.total_players = 4
        self.total_mafias = 1
        self.players_left = 4
        self.mafias_left = 1
        self.players_list = [('', '')] * self.total_players
        self.mafias_list = []
        self.sheriff = None
        self.doctor = None
        self.prompts = {}
        self.first_disable = False

    def change_player_num(self, player_num: int) -> None:
        self.total_players, self.players_left = player_num, player_num
        self.players_list = [('', '')] * player_num
        self.change_msd(self.players_list)

    def change_mafia_num(self, num):
        self.total_mafias = num

    def player_num_checker(self, lst: list) -> list[bool]:
        mafia, sheriff, doctor, remain = 0, 0, 0, 0
        for _, role in lst:
            if role.lower() == 'mafia':
                mafia += 1
            elif role.lower() == 'sheriff':
                sheriff += 1
            elif role.lower() == 'doctor':
                doctor += 1
            elif role.lower() == '':
                remain += 1
        
        m_left = self.total_mafias - mafia
        s_left = 1 - sheriff
        d_left = 1 - doctor
        
        # Return True if valid, False if invalid
        result = [
            m_left >= 0,  # Mafia count valid
            s_left >= 0,  # Sheriff count valid
            d_left >= 0,  # Doctor count valid
            m_left + s_left + d_left <= remain  # Enough remaining slots
        ]
        return result


    def change_players_list(self, name: str, role: str, position: int):
        if position <= 0 or position > self.total_players:
            raise ValueError("Invalid Position!")
        
        test_list = self.players_list[:]
        test_list[position-1] = (name, role)
        result = self.player_num_checker(test_list)
        
        # Use all() to check if all validations passed
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
        
        self.players_list[position-1] = (name, role)

        self.change_msd(self.players_list)


    def change_msd(self, player_list: list[tuple[str, str]]):
        self.mafias_list = []
        self.sheriff = None
        self.doctor = None
        for x, y in player_list:
            if y.lower() == 'mafia':
                self.mafias_list.append(x)
            elif y.lower() == 'sheriff':
                self.sheriff = x
            elif y.lower() == 'doctor':
                self.doctor = x
    def change_player_name(self, name: str, position: int):
        if position <= 0 or position > self.total_players:
            raise ValueError("Invalid Position!")
        _, role = self.players_list[position-1]
        self.players_list[position-1] = (name, role)
        self.change_msd(self.players_list)
        
    def change_first_disable(self):
        self.first_disable = False if self.first_disable else True

    def reset_values(self):
        self.total_players = 4
        self.total_mafias = 1
        self.players_left = 4
        self.mafias_left = 1
        self.players_list = [('', '')] * self.total_players
        self.mafias_list = []
        self.sheriff = None
        self.doctor = None
        self.prompts = {}
        self.first_disable = False