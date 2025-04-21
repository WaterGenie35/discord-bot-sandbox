from discord import Client
from discord.ext.commands import Cog


class ImageSearchCog(Cog):
    def __init__(self, bot: Client):
        self.bot_client = bot
        print("Initialized image search cog.")
