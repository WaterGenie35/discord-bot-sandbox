import os
import asyncio
from typing import List

from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from dotenv import load_dotenv

from echo_edit import EchoEditCog
from echo_message import EchoMessageCog
from image_search import ImageSearchCog
from monitor_event import MonitorEventCog
from monitor_rss import MonitorRSSCog
from skysports_news import SkySportsNewsCog


class SandboxBot:
    
    def __init__(self):
        self.intents = Intents.default()
        self.intents.message_content = True

        self.bot_client = Bot(command_prefix="/", intents=self.intents)

        self.bot_client.add_listener(self.ready_log, 'on_ready')
        self.bot_client.add_listener(self.setup_cogs, 'on_ready')
        print("Initialized sandbox box.")
    
    def run(self, token: str):
        self.bot_client.run(token=token)

    async def ready_log(self):
        print(f"Logged in as {self.bot_client.user}.")
    
    async def setup_cogs(self):
        cogs: List[Cog] = [
            EchoEditCog,
            EchoMessageCog,
            ImageSearchCog,
            MonitorEventCog,
            MonitorRSSCog,
            SkySportsNewsCog
        ]
        await asyncio.gather(*[self.bot_client.add_cog(cog(self.bot_client)) for cog in cogs])
        await self.bot_client.tree.sync()


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
