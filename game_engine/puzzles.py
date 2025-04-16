# puzzles.py

"""
Puzzle data models and helper logic for retrieving or updating puzzles in the database.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Puzzle(Base):
    """
    Represents a puzzle stored in the database.
    """
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)  # visible to player
    context = Column(Text, nullable=False)      # hidden environment info
    solution = Column(Text, nullable=False)
    hints = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Puzzle id={self.id} title={self.title}>"

def get_puzzle_by_id(db_session, puzzle_id):
    """
    Retrieve a Puzzle object by its ID.
    """
    return db_session.query(Puzzle).filter(Puzzle.id == puzzle_id).first()

def list_all_puzzles(db_session):
    """
    Retrieve all puzzles from the database.
    """
    return db_session.query(Puzzle).all()
