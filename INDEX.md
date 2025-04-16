# TextGame Project Index

## Project Structure
```
TextGame/
├── game_engine/           # Core game engine components
│   ├── ai_integration.py  # AI puzzle generation and solving
│   ├── cli.py            # Command line interface
│   ├── puzzle_generator.py # Puzzle generation logic
│   ├── puzzles.py        # Puzzle definitions and management
│   ├── states.py         # Game state management
│   ├── config.py         # Configuration settings
│   ├── db.py            # Database operations
│   └── __init__.py
├── utils/                # Utility scripts
│   └── create_postgres_docker.sh  # PostgreSQL Docker setup
├── tests/               # Test suite
├── venv/               # Virtual environment
├── upload_puzzles.py   # Puzzle upload script
├── setup.py           # Package installation
├── .env              # Environment variables
└── .env.example      # Environment variables template
```

## Key Components

### Game Engine
- `ai_integration.py`: AI-powered puzzle generation and solving
- `puzzle_generator.py`: Core puzzle generation logic
- `puzzles.py`: Puzzle definitions and management
- `states.py`: Game state management
- `cli.py`: Command line interface
- `db.py`: Database operations
- `config.py`: Configuration settings

### Utilities
- `create_postgres_docker.sh`: PostgreSQL Docker container setup script
- `upload_puzzles.py`: Script for uploading puzzles to database

### Setup
- `setup.py`: Package installation configuration
- `.env`: Environment configuration
- `venv/`: Python virtual environment 