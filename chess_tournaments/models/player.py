"""Player Models"""

# Module import
from tinydb import TinyDB


class Player:

    def __init__(self, PID: int, last_name: str, first_name: str, birthday: str, gender: str, rank: int):
        """Initialization of last name, first name, date of birth, gender, national identification number and rank."""
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday
        self.PID = PID
        self.gender = gender
        self.rank = rank
        self.score = 0.0
        self.opponents = []

        self.player_db = TinyDB('database/players.json')

    def serialize_player(self):
        """Return to dictionnary player info."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.birthday,
            "id": self.PID,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "opponents": self.opponents
        }

    def save_player_db(self):
        """Save new player to database set player ID as document ID."""
        players_db = self.player_db
        self.PID = players_db.insert(self.serialize_player())
        players_db.update({'id': self.PID}, doc_ids=[self.PID])

    def update_player_db(self, info, option):
        """Update player info (from user input) in database.

        Args:
            info: user input (str, or int inf "rank").
            option: update info category.
        """
        db = self.player_db
        if option == "rank":
            db.update({option: int(info)}, doc_ids=[self.PID])
        else:
            db.update({option: info}, doc_ids=[self.PID])

    @staticmethod
    def load_player_db():
        """Load player database.

        Args:
            return list of players.
        """
        players_db = TinyDB('database/players.json')
        players = players_db.all()
        return players
