"""Meun Views"""


class MenuViews:
    """Define a class Menu Views."""

    def __init__(self):
        pass

    @staticmethod
    def app_title():
        print("\n\n----------------------------------")
        print("        CHESS TOURNAMENTS")
        print("----------------------------------")

    @staticmethod
    def main_menu():
        print("\n\n=== MAIN MENU ===\n")
        print("[1] Create new tournament")
        print("[2] Resume tournament")
        print("[3] Create new player")
        print("[4] Edit existing player")
        print("[5] Reports")
        print("\n[exit] Exit program")

    @staticmethod
    def create_tournament_header():
        print("\n" * 3 + "--- NEW TOURNAMENT ---")

    @staticmethod
    def time_control_options():
        print("\nSelect time control :")
        print("[1] Bullet")
        print("[2] Blitz")
        print("[3] Rapid")
        print("\n[q] Back to main menu")

    @staticmethod
    def review_tournament(info, players):
        """Display all input info to review before saving to database.

        Args:
            info: input info list.
            players: list of selected players.
        """
        print("\n\nNew tournament created :\n")
        print(f"{info[0].upper()}, {info[1].title()}", end=' | ')
        print(f"Description : {info[2]}", end=' | ')
        print("Rounds : 4", end=' | ')
        print(f"Time control : {info[3]}")
        print("\nPlayers (8 total) :\n")

        for item in players:
            print(f"Player {players.index(item) + 1} : ", end='')
            print(f"{item['id']}", end=' | ')
            print(f"{item['last_name']}, {item['first_name']}", end=' | ')
            print(f"{item['date_of_birth']}", end=' | ')
            print(f"Rank : {item['rank']}")

        print("\nSave to database ? [y/n] ", end='')

    @staticmethod
    def tournament_saved():
        print("\nTournament successfully saved to database !")

    @staticmethod
    def start_tournament_prompt():
        print("\nStart tournament now ? [y/n] ", end='')

    @staticmethod
    def select_players(players, player_number):
        """Display all players to select.

        Args:
            players: list of players.
            player_number: number of current player for new tournament (if editing player == "").
        """
        print(f"\nSelect player {player_number} :\n")
        for i in range(len(players)):
            print(f"[{players[i]['id']}]", end=' ')
            print(f"{players[i]['last_name']}, {players[i]['first_name']}", end=" | ")
            print(f"{players[i]['gender']} | {players[i]['date_of_birth']}", end=" | ")
            print(f"Rank : {players[i]['rank']}")

        print("\n[q] Back to main menu")

    @staticmethod
    def select_tournament(tournaments):
        """Display all tournaments to select.

        Args:
            tournaments: tournaments list.
        """
        print("\n" * 3 + "--- SELECT TOURNAMENT ---\n")

        for i in range(len(tournaments)):
            print(f"[{tournaments[i]['id']}]", end=' ')
            print(tournaments[i]['name'], end=' | ')
            print(tournaments[i]['location'], end=" | ")
            print(tournaments[i]['description'], end=' | ')
            print(f"Started on : {tournaments[i]['start_date']}", end=' | ')
            print(f"Ended on : {tournaments[i]['end_date']}", end=' | ')
            print(f"Round {tournaments[i]['current_round']-1}/{tournaments[i]['rounds_total']}")

        print("\n[q] Back to main menu")

    @staticmethod
    def create_new_player_header():
        print("\n" * 3 + "- NEW PLAYER -\n")

    @staticmethod
    def review_player(info):
        """Display all input info to review before saving to database.

        Args:
            info: player info list.
        """
        print("\n\nNew player created :\n")
        print(f"{info[0]}, {info[1]}", end=' | ')
        print(f"Date of birth : {info[2]}", end=' | ')
        print(f"Gender : {info[3]}", end=' | ')
        print(f"Rank : {info[4]}")
        print("\nSave to database ? [y/n] ", end='')

    @staticmethod
    def update_player_info(player, options):
        """Player info editing prompts.

        Args:
            player: currently edited player
            options: editable options
        """
        print("\n\n--- UPDATE PLAYER INFO ---\n")
        print(f"Updating {player.last_name}, {player.first_name}\n")
        for i in range(len(options)):
            print(f"[{i+1}] Update {options[i]}")

        print("\n[q] Back to main menu")

    @staticmethod
    def player_saved():
        print("\nPlayer successfully saved to database !")

    @staticmethod
    def reports_menu():
        print("\n" * 3 + "--- REPORTS ---\n")
        print("[1] All players")
        print("[2] Players in a tournament")
        print("[3] All tournaments")
        print("[4] Rounds in a tournament")
        print("[5] Matches in a tournament")
        print("\n[q] Back to main menu")

    @staticmethod
    def reports_player_sorting():
        print("\n[1] Sort by name")
        print("[2] Sort by rank")
        print("\n[q] Back to main menu")

    @staticmethod
    def input_prompt_text(option):
        print(f"\nEnter {option} (type [q] for main menu) : ", end='')

    @staticmethod
    def input_prompt():
        print("\nType [option] and press Enter : ", end='')

    @staticmethod
    def are_you_sure_exit():
        print("\nAre you sure you want to exit the program ? [y/n] ", end='')

    @staticmethod
    def input_error():
        print("\nInput error, please enter a valid option.")

    @staticmethod
    def player_already_selected():
        print("\nPlayer already selected. Please select other player.")

    @staticmethod
    def other_report():
        print("\nWould you like to view another report ? [y/n] ", end='')

    @staticmethod
    def update_rank():
        print("\nUpdate ranks ? [y/n] ", end='')

    @staticmethod
    def rank_update_header(player):
        print(f"\nUpdating {player.last_name}, {player.first_name}")

    def input_with_validation(self, prompt, validation_func):
        """Input with validation.
        
        Args:
            prompt: prompt to display.
            validation_func: function to validate the input.
            return: validated user input.
        """
        while True:
            self.input_prompt_text(prompt)
            user_input = input()
            if validation_func(user_input):
                return user_input
            else:
                self.input_error()
    
    def input_name(self, name_type):
        """Input name (last or first).
        
        Args:
            name_type: last or first.
            return: validated name.
        """
        return self.input_with_validation(f"{name_type} name", self.validate_name)
    
    @staticmethod
    def validate_name(name):
        """Validate name (no digits).

        Args:
            name: name string to validate.
            return: True if the name contains only letters, False otherwise.
        """
        return name.isalpha()
    
    def input_rank(self):
        """Input player rank.

        Returns:
            rank: The rank of the player.
        """
        while True:
            rank_input = input("Enter rank (type [q] for main menu) : ")
            if rank_input.lower() == "q":
                self.back_to_menu()

            if rank_input.isdigit():
                return int(rank_input)
            else:
                print("Invalid input. Please enter a valid rank.")

    def input_birthday(self):
        """Input player birthday.
        
        returns:
            birthday: The date of birthday.
        """
        while True:
            birthday = input("Enter birthday (dd/mm/yyyy) (type [q] for main menu) : ")
            if birthday.lower() == "q":
                self.back_to_menu()
            try:
                self.validate_birthday_format(birthday)
                self.validate_birthday(birthday)
                return birthday
            except ValueError as e:
                print(str(e))

    def back_to_menu(self):
        from chess_tournaments.controllers.menu import MenuController
        MenuController().main_menu_start()

    @staticmethod
    def validate_birthday_format(birthday):
        parts = birthday.split('/')
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise ValueError("Invalid date format. Please use dd/mm/yyyy format.")






