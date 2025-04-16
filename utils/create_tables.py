# create_tables.py (as a standalone script, optional)
"""
Creates all tables in the DB schema.
"""

from game_engine.db import engine
from game_engine.puzzles import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
