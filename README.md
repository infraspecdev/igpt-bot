igpt-bot is a ChatGPT bot for discord. It makes ChatGPT available over Discord DMs.

## Prerequisites

1. Python 3
2. Conda (the instructions assume you use conda, but venv works too. activate env and download deps accordingly)

## Prep

1. Generate Open AI API key.
2. Create Discord bot as documented in the `Step 2 - Create a simple discord bot` section here[https://www.infraspec.dev/blog/building-a-discord-gpt-bot/] and copy bot token.

## Running the bot

1. Clone the repository.
2. Ensure you have python 3 and conda installed on your machine.
3. Modify the keys in the `env-sample`.
4. Rename `env-sample` -> `.env`
5. Create the conda virtual environment for the bot from the environment configuration - `conda env create -f environment.yml`
6. Activate the environment with `conda activate discord-bot`. All dependencies should be installed only within the virtual environment.
7. Run `python main.py` to start the bot.

## Limitations

1. The bot responds only to DMs. Cannot respond in chat rooms.
2. Conversation history is managed in memory. Upon restarting, conversation history will be lost.
