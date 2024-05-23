import discord
import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

ROLE = "role"
USER = "user"
ASSISTANT = "assistant"
SYSTEM = "system"
CONTENT = "content"

GPT_MODEL = "gpt-3.5-turbo"
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)

openAIClient = OpenAI(
  # organization='org-gMHRXBUGG89jZIWwvFwO9vR8',
  # project='proj_OB9WRw99Ff0RVgtgFQuuhr1W',
)

#todo: retain message history on a user level
#todo: do not exceed token limit
#todo: persist context and retrieve later
chat_messages = {}
def forward_user_message(author: discord.User, user_message: str) -> ChatCompletion:
    if author.id not in chat_messages:
        chat_messages[author.id] = []
    chat_messages[author.id].append({ROLE: USER, CONTENT: user_message})
    completion_response = openAIClient.chat.completions.create(
        model=GPT_MODEL,
        messages=chat_messages[author.id]
    )
    chat_messages[author.id].append({ROLE: ASSISTANT, CONTENT: completion_response.choices[0].message.content})
    return completion_response

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
async def on_message(message):
        # todo: nest properly after debugging
        if (type(message.channel) != discord.channel.DMChannel):
            return
        if message.author == discordClient.user:
            return
        else:
            completion_response = forward_user_message(message.author, message.content)
            await message.channel.send(completion_response.choices[0].message.content)
            return

discordClient.run(DISCORD_BOT_TOKEN)
