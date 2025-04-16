#!/usr/bin/env python

from game_engine.db import get_db_session, engine
from game_engine.puzzles import Base, Puzzle

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created (or already exist).")

def insert_puzzle(db, puzzle_data):
    puzzle = Puzzle(
        title=puzzle_data["title"],
        description=puzzle_data["description"],
        context=puzzle_data["context"],
        solution=puzzle_data["solution"],
        hints=puzzle_data["hints"]
    )
    db.add(puzzle)
    db.commit()
    db.refresh(puzzle)
    print(f"✅ Inserted puzzle [{puzzle.id}]: {puzzle.title}")

def main():
    create_tables()

    puzzles = [
        {
            "title": "Surface Comms Are Down",
            "description": "You're remotely controlling a robot on the surface. The communications relay station has stopped transmitting.",
            "context": (
                "The robot is inside the communications relay station. There's a burnt-circuit smell. "
                "The antenna wires are corroded by a black substance leaking from a damaged panel. "
                "Spare wires are in a locked maintenance closet. Note says 'Maintenance code: sum of first three primes.'"
            ),
            "solution": "Locate the maintenance closet, enter code '10', replace wires, repair antenna, and reboot the relay.",
            "hints": "Check notes carefully—numerical clues often mean something specific."
        },
        {
            "title": "Locked Entryway",
            "description": "You're remotely controlling a robot that has encountered a locked entryway door blocking its path.",
            "context": (
                "Robot sees a metal door with an electronic keypad and a dusty wall sign reading: "
                "'Door code: today's date reversed.' Today's date internally registered as '0415'."
            ),
            "solution": "Enter the door code '5140' to unlock the door.",
            "hints": "Pay close attention to signs and instructions; reversal clues are common."
        },
        {
            "title": "Power Failure",
            "description": "You're guiding your robot into a main control room that's dark due to a power failure.",
            "context": (
                "Emergency lights flicker. Power distribution panel reads: 'Fuse blown—Replace fuse and reset system.' "
                "Replacement fuses are locked in a toolbox. A log nearby: 'Combination = emergency lights × 3.' "
                "Robot counts 4 emergency lights."
            ),
            "solution": "Use combination '12' to open the toolbox, replace the fuse, and reset the panel.",
            "hints": "Counting items explicitly mentioned in clues usually leads to solutions."
        }
    ]

    db_session = next(get_db_session())
    for puzzle_data in puzzles:
        insert_puzzle(db_session, puzzle_data)

if __name__ == "__main__":
    main()
