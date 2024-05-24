import unittest
from src import bot

class DiscordBotTestCase(unittest.TestCase):
    def test_is_over_token_limit(self):
        test_bot = bot.Bot("discord-key", "openai-key")
        text = "random text to tokenize"
        self.assertFalse(test_bot.is_over_token_limit(text))

    def test_is_over_message_length_limit(self):
        test_bot = bot.Bot("discord-key", "openai-key")
        text = "message to send on discord"
        self.assertFalse(test_bot.is_over_message_length_limit(text))
