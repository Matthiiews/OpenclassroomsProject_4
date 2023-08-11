"""Round Views"""


# Module Import
from prettytable import PrettyTable


class RoundViews:
    """Define a class RoundViews."""
    def __init__(self):
        """Initialization of the table."""
        self.table = PrettyTable()
        self.round_field_names = [
            "Match #",
            "Name P1",
            "Rank P1",
            "Score P1",
            " ",
            "Name P2",
            "Rank P2",
            "Score P2"
        ]

        self.results_field_names = [
            "Tournament ranking",
            "Name",
            "Final Score",
            "Global ranking"
        ]

    def display_matches(self, matches):
        """Display matches for the current round as a table.

        Args:
            matches: list of match tuples.
        """
        self.table.clear()
        self.table.field_names = self.round_field_names

        for i, match in enumerate(matches):
            row = list(match)
            row.insert(0, str(i+1))
            row.insert(4, "vs.")
            self.table.add_row(row)

        print(self.table)

    def display_results(self, tournament):
        """Display results at the end of the tournament.

        Args:
            tournament: current tournament.
        """
        self.table.clear()
        self.table.field_names = self.results_field_names

        for i, player in enumerate(tournament.players):
            self.table.add_row([
                i+1,
                f"{player['last_name']}, {player['first_name']}",
                player['score'],
                player['rank']
            ])

        print("\n\n- FINAL SCORES -\n")
        print(f"{tournament.name.upper()}, {tournament.location.title()} | Description: {tournament.description}")
        print(
            f"Start: {tournament.start_date} | End: {tournament.end_date} | Time control: {tournament.time_control}\n")

        print(self.table)

    @staticmethod
    def round_header(tournament, start_time):
        """Display tournament info as a round header.

        Args:
            tournament: current tournament.
            start_time: tournament start time (str).
        """
        print("\n\n")

        h_1 = f"{tournament.name.upper()}, {tournament.location.title()} | Description: {tournament.description}"
        h_2 = f"Start date and time: {tournament.start_date} | Time control: {tournament.time_control}\n"
        h_3 = f"- ROUND {tournament.current_round}/{tournament.rounds_total} | {start_time} -"

        print(h_1.center(100, " "))
        print(h_2.center(100, " "))
        print(h_3.center(100, " "))

    @staticmethod
    def round_over():
        print("\nRound over? [ok]")
        print("Back to the main menu? [q]")

    @staticmethod
    def score_options(match_number):
        print("\nMatch", match_number)
        print("[0] Draw")
        print("[1] Player 1 wins")
        print("[2] Player 2 wins")
        print("\n[q] Back to the main menu")

    @staticmethod
    def score_input_prompt():
        print("\nEnter result:", end=' ')
