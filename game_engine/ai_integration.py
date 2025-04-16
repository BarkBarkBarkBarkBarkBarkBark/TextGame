# ai_integration.py

"""
Handles calls to OpenAI to interpret user input,
generate story details, or validate puzzle solutions.
"""

import openai
from game_engine.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def respond_as_robot(user_input: str, environment_context: str, memory: list) -> str:
    """
    Respond as the field robot using hidden context and conversation memory.
    """
    # Start with a system message defining the robot's persona
    messages = [
        {
            "role": "system",
            "content": (
                "You are a surface exploration robot responding to a human operator underground. "
                "You have access to a hidden environmental context which represents everything in the scene. "
                "Only describe things that would be observed or inferred based on the operator's requests. "
                "Don't dump all the context at once. Reveal the environment naturally, as if the robot is exploring it in real time. "
                "Speak in a clear, concise tone. Use first person — you're the robot."
            )
        },
        {
            "role": "user",
            "content": f"Hidden environment context (not visible to player):\n{environment_context}"
        }
    ]

    # Add prior conversation
    messages.extend(memory)

    # Add new user input
    messages.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200,
        temperature=0.6
    )

    reply = response.choices[0].message.content.strip()
    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": reply})
    return reply


def interpret_command(user_input: str, game_context: str) -> str:
    """
    (Legacy / optional) Summarizes what the player is trying to do.
    Could still be used for logging, debugging, or AI command parsing.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an interpreter AI. Given a command from a human player and game context, summarize the player's intent."
        },
        {
            "role": "user",
            "content": f"Game context: {game_context}\nUser command: {user_input}\n\nRespond with a concise interpretation."
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
        max_tokens=50
    )

    return response.choices[0].message.content.strip()


def check_puzzle_solution(user_input: str, expected_solution: str) -> bool:
    """
    Uses OpenAI to strictly verify puzzle completion based on logical correctness.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are evaluating whether the user's input correctly matches the puzzle solution. "
                "Respond 'YES' if the user's input matches or logically completes the expected solution provided. "
                "Respond 'NO' otherwise. If there's a numeric or logical detail, verify it strictly."
            )
        },
        {
            "role": "user",
            "content": (
                f"Expected Solution: {expected_solution}\n\n"
                f"User Attempt: {user_input}\n\n"
                "Does the user's attempt match or logically complete the expected solution?"
            )
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=5
    )

    answer = response.choices[0].message.content.strip().upper()
    return answer == "YES"
