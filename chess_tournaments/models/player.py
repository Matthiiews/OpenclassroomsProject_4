"""Player Models"""

# Module import
from tinydb import TinyDB
from datetime import datetime
import re


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

    def create_player(self) -> None:
        """Created a new player."""
        self.validate_name(self.last_name)
        self.validate_name(self.first_name)
        self.validate_birthday(self.birthday)
        
        if self.PID is not None:
            self.validate_pid(self.PID)
        return self

    def serialize_player(self) -> dict:
        """Return dictionary player info."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.birthday,
            "PID": self.PID,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "opponents": self.opponents
        }

    def save_player_db(self) -> None:
        """Save new player to database set player ID as document ID."""
        players_db = self.player_db
        player_info = self.serialize_player()
        self.PID = players_db.insert(player_info)
        players_db.update(player_info, doc_ids=[self.PID])

    def update_player_db(self, info, option):
        """Update player info (from user input) in database.

        Args:
            info: user input (str, or int inf "rank").
            option: update info category.
        """
        db = self.player_db
        player_info = {option: int(info) if option == "rank" else info}
        db.update(player_info, doc_ids=[self.PID])

    @staticmethod
    def load_player_db() -> list:
        """Load player database.

        Returns:
            return list of players.
        """
        players_db = TinyDB('database/players.json')
        players = players_db.all()
        return players

    @staticmethod
    def validate_name(name) -> None:
        """Validates the player's name."""
        if not name:
            raise ValueError("The name of the player cannot be empty.")
        return True

    @staticmethod
    def validate_birthday(birthday) -> None:
        """Validates the date of birth format
        
        Args:
            birthday: date of birth (str).
            return: True if the date is in the correct format: False otherwise.
        """
        try:
            datetime.strptime(birthday, "%d/%m/%Y")
        except ValueError:
            raise ValueError("date of birth format must be dd/mm/yyyy")
        return True

    @staticmethod
    def validate_pid(pid) -> None:
        """Validates the PID (Player ID)."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", pid):
            raise ValueError("The PID can only contain letters, dash, numbers and underscores.")
        return True
    
    @staticmethod
    def validate_rank(rank: int) -> None:
        """Validates the rank."""
        if rank < 1 or rank > 100:
            raise ValueError("The rank must be between 1 and 100.")
        return True
        