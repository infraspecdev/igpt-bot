import discord
import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

intents = discord.Intents.default()
intents.message_content = True

discordClient = discord.Client(intents=intents)

openAIClient = OpenAI(
  # organization='org-gMHRXBUGG89jZIWwvFwO9vR8',
  # project='proj_OB9WRw99Ff0RVgtgFQuuhr1W',
)

def forward_user_message(user_message: str) -> ChatCompletion:
    completion_response = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return completion_response

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
async def on_message(message):
    if message.author == discordClient.user :
        return
    else:
        print(message)
        print(type(message.channel))
        print("forwarding message to chatpgt")
        completion_response = forward_user_message(message.content)
        await message.channel.send(completion_response.choices[0].message.content)
discordClient.run(os.getenv('DISCORD_BOT_TOKEN'))
