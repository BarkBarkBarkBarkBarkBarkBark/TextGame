# states.py

"""
Game state management for tracking the player's progress.
"""

class GameState:
    """
    Holds the player's current status: location, puzzles completed,
    inventory, etc.
    """

    def __init__(self):
        self.location = "Start"
        self.completed_puzzles = set()
        self.inventory = []

    def move_to(self, new_location: str):
        """
        Move the player to a different location.
        """
        self.location = new_location

    def complete_puzzle(self, puzzle_id: int):
        """
        Mark a puzzle as completed.
        """
        self.completed_puzzles.add(puzzle_id)

    def has_completed(self, puzzle_id: int) -> bool:
        """
        Check if a puzzle is already completed.
        """
        return puzzle_id in self.completed_puzzles
