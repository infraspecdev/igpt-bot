import discord
import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from loguru import logger
import tiktoken

ROLE = "role"
USER = "user"
ASSISTANT = "assistant"
SYSTEM = "system"
CONTENT = "content"

GPT_MODEL = "gpt-3.5-turbo"
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

MAX_TOKEN_LENGTH = 4096

#todo: extract discord client as a separate class, wrapper on top of discord client type
def create_discord_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

#todo: extract openAI client as a separate class, wrapper on top of openAI type
def create_openAI_client() -> OpenAI:
    client = OpenAI()
    return client

class Bot:
    def __init__(self, discord_client, openAI_client):
        self.discord_client = discord_client
        self.openAI_client = openAI_client
        self.chat_messages = {}

    def is_over_token_limit(self, text: str) -> bool:
        encoding = tiktoken.encoding_for_model(GPT_MODEL)
        count = len(encoding.encode(text))
        return count > MAX_TOKEN_LENGTH

    def forward_user_message(self, user_message: discord.Message) -> str:
        if self.is_over_token_limit(user_message.content):
            #todo: display warning message
            return "Your text has exceeded the request token limit; Please provide a shorter text"
            return

        author = user_message.author
        if author.id not in self.chat_messages:
            self.chat_messages[author.id] = []

        self.chat_messages[author.id].append({ROLE: USER, CONTENT: user_message.content})
        completion_response = self.openAI_client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.chat_messages[author.id]
        )
        assistant_message = completion_response.choices[0].message.content
        if self.is_over_token_limit(assistant_message):
            #summarise and append summarised text
            summarised_text = "summarised_text"
            self.chat_messages[author.id].append({ROLE: ASSISTANT, CONTENT: summarised_text})
        else:
            self.chat_messages[author.id].append({ROLE: ASSISTANT, CONTENT: completion_response.choices[0].message.content})

        logger.debug(self.chat_messages)
        return completion_response.choices[0].message.content

    def run(self):
        @self.discord_client.event
        async def on_ready():
            logger.info('We have logged in as {0.user}'.format(self.discord_client))

        @self.discord_client.event
        async def on_message(message: discord.Message):
                # todo: nest properly after debugging
                if (type(message.channel) != discord.channel.DMChannel):
                    return
                if message.author == self.discord_client.user:
                    return
                else:
                    response = self.forward_user_message(message)
                    await message.channel.send(response) # handle for discord's character limit (2000 chars)
                    return

        self.discord_client.run(DISCORD_BOT_TOKEN)
