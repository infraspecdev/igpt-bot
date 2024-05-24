from src.discord_bot import bot

chatgpt_discord_bot = bot.Bot(bot.create_discord_client(), bot.create_openAI_client())
chatgpt_discord_bot.run()
