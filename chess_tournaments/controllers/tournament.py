"""Tournament Controller"""

# Module Import
from datetime import datetime
from chess_tournaments.models.player import Player
from chess_tournaments.models.round import Round
from chess_tournaments.views.round import RoundViews
from chess_tournaments.views.menu import MenuViews


class TournamentController:
    """Define a class Tournament Controller"""
    def __init__(self):
        self.menu_view = MenuViews()
        self.round_view = RoundViews()
        self.timer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_tournament(self, tournament):
        """Tournament (tournament) main structure.
        Start from first round or resume tournament according to round number.
        Set start and end timers and save to DB.
        """
        if tournament.current_round == 1:
            tournament.start_date = self.timer
            tournament.update_timer(tournament.start_date, 'start_date')
            self.first_round(tournament)
            tournament.current_round += 1
            tournament.update_tournament_db()

            while tournament.current_round <= tournament.rounds_total:
                self.next_rounds(tournament)
                tournament.current_round += 1
                tournament.update_tournament_db()

        elif 1 < tournament.current_round <= tournament.rounds_total:
            while tournament.current_round <= tournament.rounds_total:
                self.next_rounds(tournament)
                tournament.current_round += 1
                tournament.update_tournament_db()

            tournament.end_date = self.timer
            tournament.update_timer(tournament.end_date, 'end_date')
            self.tournament_end(tournament)

        elif tournament.current_round > tournament.rounds_total:
            self.tournament_end(tournament)

    def first_round(self, tournament):
        """First round : top players vs. bottom players
        Get pairings and set round to save to DB.
        """
        round_ = Round("Round 1", self.timer, "TBD")
        tournament.sort_players_by_rank()
        top_players, bottom_players = tournament.split_players()
        self.round_view.round_header(tournament, round_.start_datetime)

        for i in range(tournament.rounds_total):
            round_.get_match_pairing(top_players[i], bottom_players[i])
            top_players[i], bottom_players[i] = self.update_opponents(top_players[i], bottom_players[i])

        self.round_view.display_matches(round_.matches)

        self.round_view.round_over()
        self.menu_view.input_prompt()
        user_input = input().lower()
        scores_list = []

        if user_input == "ok":
            round_.end_datetime = self.timer
            tournament.rounds.append(round_.set_round())
            tournament.merge_players(top_players, bottom_players)

            self.end_of_round(scores_list, tournament)

        elif user_input == "q":
            self.back_to_menu()

    def next_rounds(self, tournament):
        """Next rounds : set possible pairings
        Get pairings and set round to save to DB.
        """
        round_ = Round(("Round " + str(tournament.current_round)), self.timer, "TBD")
        tournament.sort_players_by_score()
        self.round_view.round_header(tournament, round_.start_datetime)

        available_list = tournament.players
        players_added = []

        k = 0
        while k < tournament.rounds_total:
            if available_list[1]["id"] in available_list[0]["opponents"]:
                try:
                    available_list, players_added = self.match_other_option(available_list, players_added, round_)
                    tournament.players = players_added

                except IndexError:
                    available_list, players_added = self.match_first_option(available_list, players_added, round_)
                    tournament.players = players_added

            elif available_list[1]["id"] not in available_list[0]["opponents"]:
                available_list, players_added = self.match_first_option(available_list, players_added, round_)
                tournament.players = players_added

            k += 1

        self.round_view.display_matches(round_.matches)

        self.round_view.round_over()
        self.menu_view.input_prompt()
        user_input = input().lower()
        scores_list = []

        if user_input == "ok":
            round_.end_datetime = self.timer
            tournament.rounds.append(round_.set_round())
            self.end_of_round(scores_list, tournament)

        elif user_input == "q":
            self.back_to_menu()

    def match_first_option(self, available_list, players_added, round_):
        """Main pairing option.

        Args:
            available_list: list of players not set in match for current round.
            players_added: list of players already in match for current round.
            round_: current round.
            return: updated lists.
        """
        round_.get_match_pairing(available_list[0], available_list[1])
        available_list[0], available_list[1] = self.update_opponents(available_list[0], available_list[1])
        available_list, players_added = self.update_player_lists(
            available_list[0],
            available_list[1],
            available_list,
            players_added
        )
        return available_list, players_added

    def match_other_option(self, available_list, players_added, round_):
        """Alternative pairing option.

        Args:
            available_list: list of players not set in match for current round.
            players_added: list of players already in match for current round.
            round_: current round.
            return: updated lists.
        """
        round_.get_match_pairing(available_list[0], available_list[2])
        available_list[0], available_list[2] = self.update_opponents(available_list[0], available_list[2])
        available_list, players_added = self.update_player_lists(
            available_list[0],
            available_list[2],
            available_list,
            players_added
        )

        return available_list, players_added

    def end_of_round(self, scores_list: list, tournament):
        """End of round : update player scores.

        Args:
            tournament: current tournament.
            scores_list: list of scores.
            return: players list with updated scores.
        """
        for i in range(tournament.rounds_total):
            self.round_view.score_options(i + 1)
            response = self.input_scores()
            scores_list = self.get_score(response, scores_list)

        tournament.players = self.update_scores(tournament.players, scores_list)

        return tournament.players

    def input_scores(self):
        """Score input."""
        self.round_view.score_input_prompt()
        response = input()
        return response

    def get_score(self, response, scores_list: list):
        """Input scores for each match in current round.

        Args:
            response: user input (str).
            scores_list: list of scores.
            return: updated list of scores.
        """
        if response == "0":
            scores_list.extend([0.5, 0.5])
            return scores_list
        elif response == "1":
            scores_list.extend([1.0, 0.0])
            return scores_list
        elif response == "2":
            scores_list.extend([0.0, 1.0])
            return scores_list
        elif response == "q":
            self.back_to_menu()
        else:
            self.menu_view.input_error()
            self.input_scores()

    @staticmethod
    def update_scores(players, scores_list: list):
        """Update player scores.

        Args:
            players: list of players.
            scores_list: list of scores.
            return: list of players with updated scores.
        """
        for i in range(len(players)):
            players[i]["score"] += scores_list[i]

        return players

    @staticmethod
    def update_player_lists(player_1, player_2, available_list, players_added):
        """Update player lists :
        Add unavailable player to respective list.
        Remove available player form respective list.

        Args:
            player_1: player 1 (dict).
            player_2: player 2 (dict).
            available_list: list of players not set in match for current round.
            players_added: list of players already in match for current round.
            return: list of available players, list of unavailable players.
        """
        players_added.extend([player_1, player_2])
        available_list.remove(player_1)
        available_list.remove(player_2)

        return available_list, players_added

    @staticmethod
    def update_opponents(player_1, player_2):
        player_1["opponents"].append(player_2["id"])
        player_2["opponents"].append(player_1["id"])

        return player_1, player_2

    def tournament_end(self, tournament):
        """End of tournament : display final results.
        Offer user to update ranks.

        Args:
            tournament: current tournament dict.
        """
        tournament.sort_players_by_rank()
        tournament.sort_players_by_score()

        self.round_view.display_results(tournament)

        self.menu_view.update_rank()
        user_input = input()

        if user_input == "n":
            self.back_to_menu()

        elif user_input == "y":
            while True:
                self.update_ranks(tournament.players)

    def update_ranks(self, players):
        """Update player ranks and save to DB.

        Args:
            players: tournament player list.
        """
        self.menu_view.select_players(players, "to update")
        self.menu_view.input_prompt()
        user_input = input()

        if user_input == "q":
            self.back_to_menu()

        for i in range(len(players)):
            if int(user_input) == players[i]["id"]:
                p = players[players.index(players[i])]
                p = Player(
                    p['id'],
                    p['last_name'],
                    p['first_name'],
                    p['date_of_birth'],
                    p['gender'],
                    p['rank']
                )

                self.menu_view.rank_update_header(p)
                new_rank = self.menu_view.input_with_validation("new rank", lambda rank: rank.isdigit())

                try:
                    p.update_player_db(int(new_rank), "rank")
                    players[i]["rank"] = int(new_rank)
                    print(f"Player {p.first_name} {p.last_name}'s rank updated successfully!")
                except ValueError as ve:
                    print(f"Error updating player rank: {str(ve)}")

        user_input = input()

        if user_input == "q":
            self.back_to_menu()

    @staticmethod
    def back_to_menu():
        from chess_tournaments.controllers.menu import MenuController
        MenuController().main_menu_start()

    def add_new_player(self):
        """Adds a new player."""
        self.menu_view.input_prompt_text("last_name")
        last_name = input()
        self.menu_view.input_prompt_text("first_name")
        first_name = input()
        self.menu_view.input_prompt_text("birthday (format : dd/mm/jj)")
        birthday = input()
        self.menu_view.input_prompt_text("gender")
        gender = input()

        try:
            new_player = Player(last_name, first_name, birthday, gender).create_player()
            print(f"Player {new_player.first_name} {new_player.last_name} was created successfully!")
        except ValueError as ve:
            print(f"Error when creating the player: {str(ve)}")
