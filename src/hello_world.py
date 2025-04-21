import os

from discord import Intents
from discord import Message
from discord.ext.commands import Bot
from dotenv import load_dotenv


class SandboxBot:
    
    def __init__(self):
        self.intents = Intents.default()
        self.intents.message_content = True

        self.bot_client = Bot(command_prefix="/", intents=self.intents)
        
        self.bot_client.add_listener(self.on_ready, 'on_ready')
        self.bot_client.add_listener(self.echo_message, 'on_message')
        print("Initialized sandbox box.")
    
    def run(self, token: str):
        self.bot_client.run(token=token)

    async def on_ready(self):
        print(f"Logged in as {self.bot_client.user}")
    
    async def echo_message(self, message: Message):
        if message.author == self.bot_client.user:
            return
        author = message.author
        channel = message.channel
        message_location = f"{channel.category}|{channel.name}" if channel.category else channel.name
        print(f"[{message_location}] {author.display_name} ({author.name}): {message.content}")


def main():
    load_dotenv()
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        print("Could not load discord bot token from environment file.")
        print("Please specify the token in .env file under the key DISCORD_BOT_TOKEN.")
        return

    bot = SandboxBot()
    bot.run(bot_token)


if __name__ == '__main__':
    main()
