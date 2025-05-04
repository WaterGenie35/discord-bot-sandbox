from discord import Message
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog


class EchoEditCog(Cog):
    
    def __init__(self, bot: Bot):
        self.bot_client = bot
        print("Initialized echo edit cog.")
    
    @commands.Cog.listener('on_message_edit')
    async def echo_edit(self, before: Message, after: Message):
        if before.author == self.bot_client.user:
            return
        if before.content == after.content:
            return
        author = after.author
        channel = after.channel
        message_location = f"{channel.category}|{channel.name}" if channel.category else channel.name
        print(f"[{message_location}] {author.display_name} ({author.name}) edited:")
        print(f"  From: {before.content}")
        print(f"    To: {after.content}")
