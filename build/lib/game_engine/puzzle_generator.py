#!/usr/bin/env python

import os
import openai
import re

from game_engine.config import OPENAI_API_KEY
from game_engine.db import get_db_session, engine
from game_engine.puzzles import Base, Puzzle
from sqlalchemy.exc import IntegrityError

openai.api_key = OPENAI_API_KEY

if not openai.api_key:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit(1)

# Ensure the puzzle table exists
Base.metadata.create_all(bind=engine)

def generate_text_puzzle(prompt: str) -> str:
    """
    Generate a puzzle using GPT, formatted with a hidden context section.
    """
    system_message = (
        "You are a creative puzzle generator for a text-based command-line game. "
        "When creating puzzles, use plain language that does not rely on wordplay"
        "Generate a simple puzzle using the following format:\n\n"
        "Title: <short title>\n"
        "Description: <brief intro given to player>\n"
        "Context: <hidden info known only to the system — describe the environment and all clues>\n"
        "Solution: <the correct steps to solve the puzzle>\n"
        "Hints: <optional hints the player could get later>\n\n"
        "Only return the puzzle in this format."
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def parse_puzzle_fields(puzzle_text: str):
    """
    Extract puzzle components from GPT response.
    """
    title_match = re.search(r"(?i)Title:\s*(.*)", puzzle_text)
    desc_match = re.search(r"(?i)Description:\s*(.*)", puzzle_text)
    context_match = re.search(r"(?i)Context:\s*(.*)", puzzle_text)
    soln_match = re.search(r"(?i)Solution:\s*(.*)", puzzle_text)
    hints_match = re.search(r"(?i)Hints?:\s*(.*)", puzzle_text)

    title = title_match.group(1).strip() if title_match else "Untitled Puzzle"
    description = desc_match.group(1).strip() if desc_match else "No description"
    context = context_match.group(1).strip() if context_match else "No context"
    solution = soln_match.group(1).strip() if soln_match else "No solution"
    hints = hints_match.group(1).strip() if hints_match else ""

    return title, description, context, solution, hints

def insert_puzzle_into_db(title, description, context, solution, hints):
    """
    Insert the puzzle with hidden context into the DB.
    """
    session_gen = get_db_session()
    db = next(session_gen)
    try:
        new_puzzle = Puzzle(
            title=title,
            description=description,
            context=context,
            solution=solution,
            hints=hints
        )
        db.add(new_puzzle)
        db.commit()
        db.refresh(new_puzzle)
        puzzle_id = new_puzzle.id
    except IntegrityError as e:
        db.rollback()
        puzzle_id = None
        print("Error inserting puzzle:", e)
    finally:
        db.close()

    return puzzle_id

def main():
    print("Welcome to the OpenAI Puzzle Generator!")
    user_input = input("Enter a theme or prompt for the puzzle: ").strip()

    puzzle_text = generate_text_puzzle(user_input)
    print("\nGenerated Puzzle Text:\n", puzzle_text)

    title, description, context, solution, hints = parse_puzzle_fields(puzzle_text)

    print("\nParsed Fields:")
    print("Title:", title)
    print("Description:", description)
    print("Context:", context)
    print("Solution:", solution)
    print("Hints:", hints)

    puzzle_id = insert_puzzle_into_db(title, description, context, solution, hints)

    if puzzle_id:
        print(f"\n✅ Puzzle successfully added to the database with ID: {puzzle_id}")
    else:
        print("\n❌ Failed to add puzzle to the database.")

if __name__ == "__main__":
    main()
