from discord import Message
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog


class EchoMessageCog(Cog):
    
    def __init__(self, bot: Bot):
        self.bot_client = bot
        print("Initialized echo message cog.")
    
    @commands.Cog.listener('on_message')
    async def echo_message(self, message: Message):
        if message.author == self.bot_client.user:
            return
        if message.content.startswith(self.bot_client.command_prefix):
            return

        author = message.author
        channel = message.channel
        message_location = f"{channel.category}|{channel.name}" if channel.category else channel.name
        print(f"[{message_location}] {author.display_name} ({author.name}): {message.content}")
