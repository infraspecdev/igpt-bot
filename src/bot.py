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

def create_discord_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

def create_openAI_client() -> OpenAI:
    client = OpenAI()
    return client


    # encoding = tiktoken.encoding_for_model(GPT_MODEL)

    #todo: do not exceed token limit
    #todo: persist context and retrieve later
    # def summarize_text(text: str)-> str:

    #     return ""

    # def count_tokens(text: str)-> int:
    #     count = len(encoding.encode(chat_messages[author.id]))
    #     return count


class Bot:
    def __init__(self, discord_client, openAI_client):
        self.discord_client = discord_client
        self.openAI_client = openAI_client
        self.chat_messages = {}
        print(">>> Inititalised here")
        print(">>> {0}".format(self.discord_client))
        print(">>> {0}".format(self.openAI_client))

    def forward_user_message(self, author: discord.User, user_message: str) -> ChatCompletion:
        # user_message_tokens = count_tokens(user_message)
        # if user_message_tokens > MAX_TOKEN_LENGTH :
        #     print("exceeded token limits; please shorten your query text")

        if author.id not in self.chat_messages:
            self.chat_messages[author.id] = []

        self.chat_messages[author.id].append({ROLE: USER, CONTENT: user_message})
        completion_response = self.openAI_client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.chat_messages[author.id]
        )
        self.chat_messages[author.id].append({ROLE: ASSISTANT, CONTENT: completion_response.choices[0].message.content})
        logger.debug(self.chat_messages)
        logger.info(completion_response)
        return completion_response

    # def register_events(self):


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
                    completion_response = self.forward_user_message(message.author, message.content)
                    await message.channel.send(completion_response.choices[0].message.content)
                    return

        self.discord_client.run(DISCORD_BOT_TOKEN)
