import os
import discord
from dotenv import load_dotenv


class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        
    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f"Message from {message.author}: {message.content}")


def main():
    load_dotenv()
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        print("Could not load discord bot token from environment file.")
        print("Please specify the token in .env file under the key DISCORD_BOT_TOKEN.")
        return

    message_intent = discord.Intents.default()
    message_intent.message_content = True

    client = BotClient(intents=message_intent)
    client.run(token=bot_token)


if __name__ == '__main__':
    main()
