# cli.py

from game_engine.db import get_db_session
from game_engine.puzzles import get_puzzle_by_id, list_all_puzzles
from game_engine.states import GameState
from game_engine.ai_integration import respond_as_robot, check_puzzle_solution  # updated import

def choose_puzzle():
    """
    Present all available puzzles and allow the user to select one by ID.
    """
    with next(get_db_session()) as db:
        puzzles = list_all_puzzles(db)
        if not puzzles:
            print("No puzzles found in the database.")
            return None

        print("Available Puzzles:")
        for puzzle in puzzles:
            print(f"[{puzzle.id}] {puzzle.title}")

        while True:
            try:
                choice = int(input("\nEnter the ID of the puzzle you'd like to play: ").strip())
                puzzle = get_puzzle_by_id(db, choice)
                if puzzle:
                    return puzzle
                print("Invalid puzzle ID. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

def main():
    state = GameState()
    puzzle = choose_puzzle()
    if not puzzle:
        return

    print(f"\n--- Now playing: {puzzle.title} ---")
    print(f"{puzzle.description}\n")

    memory = []  # Holds chat history with the robot

    while True:
        user_input = input("> ")
        if user_input.lower() in ("quit", "exit"):
            print("Exiting the game. Goodbye!")
            break

        robot_reply = respond_as_robot(user_input, puzzle.context, memory)
        print(f"Robot: {robot_reply}")

        if check_puzzle_solution(user_input, puzzle.solution):
            print("\n🎉 Congratulations, you've solved the puzzle!")
            state.complete_puzzle(puzzle.id)
            break

if __name__ == "__main__":
    main()
