#!/usr/bin/env bash

set -e

# Helper function to print status messages
status() {
    echo -e "\n🚀 \033[1;34m$1\033[0m\n"
}

error_exit() {
    echo -e "\n❌ \033[1;31m$1\033[0m\n"
    exit 1
}

# 1. Check Docker installation
status "Checking Docker installation..."

if ! command -v docker &> /dev/null; then
    if [ -f "/Applications/Docker.app/Contents/Resources/bin/docker" ]; then
        status "Docker CLI found in Docker.app. Adding to PATH..."
        export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
        echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    elif [ -f "/usr/local/bin/docker" ]; then
        status "Docker CLI found in /usr/local/bin. Adding to PATH..."
        export PATH="/usr/local/bin:$PATH"
        echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    else
        error_exit "Docker is not installed. Please install Docker Desktop from https://docs.docker.com/desktop/mac/install/ and run it before continuing."
    fi
fi

if ! docker info &> /dev/null; then
    error_exit "Docker Desktop is installed but not running. Please launch Docker Desktop and ensure it's fully started."
fi

status "Docker is installed and running."

# 2. Set up Python virtual environment
status "Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    status "Created new virtual environment."
fi

# Source the virtual environment in the current shell
source venv/bin/activate

# Upgrade pip
status "Upgrading pip..."
pip install --upgrade pip

# 3. Install Python package in editable mode
status "Installing Python package dependencies..."
pip install -e .

# 4. Run Docker setup script
status "Creating PostgreSQL Docker container..."

# Adjust the following variables as necessary
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
CONTAINER_NAME="climb"
DATABASE_NAME="climb"
PORT="5432"

if [ -f "./utils/create_postgres_docker.sh" ]; then
    bash ./utils/create_postgres_docker.sh \
        "$POSTGRES_USER" \
        "$POSTGRES_PASSWORD" \
        "$CONTAINER_NAME" \
        "$DATABASE_NAME" \
        "$PORT"
else
    error_exit "Could not find ./utils/create_postgres_docker.sh script. Please ensure the file exists and is executable."
fi

# 5. Create database tables
status "Creating database tables..."
python utils/create_tables.py

# 6. Upload puzzles
status "Uploading puzzles..."
python utils/upload_puzzles.py

status "🎉 Installation completed successfully! You're ready to play."

echo -e "\033[1;32mYour virtual environment is now active. Run your game with:\033[0m"
echo -e "  start-game\n"

# Keep the virtual environment active by not exiting the script
exec $SHELL
