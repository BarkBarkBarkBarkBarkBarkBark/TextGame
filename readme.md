
Install Docker desktop

Clone the repo

```
git clone https://github.com/BarkBarkBarkBarkBarkBarkBark/TextGame.git
```

Change .env.example to .env, and add openai key


navigate to directory

```
cd TextGame
```

make sure that setup script is executable, and then execute

```
chmod +x install_game.sh
./install_game.sh
```

Create Game Tables

```
python utils/create_tables.py
```

Upload some premade puzzles

```
python utils/upload_puzzles.py
```

Start the dang game

```
start-game
```