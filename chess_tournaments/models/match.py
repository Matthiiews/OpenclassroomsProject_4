""" Match Models """

class Match:
    """Define a class for individual matches"""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def get_match_pairing(self, player_1, player_2):
        ''' Return match paring as a tuple '''
        match = (
            f"{player_1['last_name']}, {player_1['first_name']}",
            player_1["rank"],
            player_1["score"],
            f"{player_2['last_name']}, {player_2['first_name']}",
            player_2["rank"],
            player_2["score"]
        )
        self.matches.append(match)
        