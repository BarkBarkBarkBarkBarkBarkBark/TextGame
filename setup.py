# setup.py

from setuptools import setup, find_packages

setup(
    name="my_game",              # The name of your project/package
    version="0.1.0",             # Project version
    packages=find_packages(),    # Automatically finds all packages with __init__.py
    install_requires=[
        "setuptools>=68.0.0",
        "docker>=6.0.0",
        "openai>=1.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",  # for CLI
        "rich>=13.0.0",  # for CLI formatting
        # Include any other dependencies you have:
        # "psycopg2-binary",  # If connecting to Postgres directly
        # "python-dotenv",    # If needed for .env file support, etc.
    ],
    entry_points={
        "console_scripts": [
            # This allows you to run `start-game` at the command line after install
            "start-game=game_engine.cli:main",
        ],
    },
    python_requires=">=3.7",     # or whichever version you require
)
