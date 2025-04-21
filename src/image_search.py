import os
import asyncio
import aiohttp

from discord import Interaction
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.permissions import Permissions


class ImageSearchCog(Cog):
    
    TIMEOUT_LIMIT = 8 # seconds
    MISSING_PROMPT_MESSAGE = "Please specify an image prompt."
    TIMEOUT_ERROR_MESSAGE = "Image search took too long, please try again later."
    SEARCH_ERROR_MESSAGE = "Could not find any images, please try again later."
    PIXABAY_URL = 'https://pixabay.com/api/'
    
    def __init__(self, bot: Bot):
        self.bot_client = bot
        self.pixabay_api_key = os.getenv('PIXABAY_API_KEY')
        if not self.pixabay_api_key:
            print("Could not load pixabay api key from environment file.")
            print("Please specify the api key in .env file under the key PIXABAY_API_KEY.")
        self.pixabay_api_params = {
            'key': self.pixabay_api_key,
            'image_type': 'photo',
            'safesearch': 'true',
            'page': 1,
            'per_page': 3
        }
        
        print("Initialized image search cog.")
    
    # TODO: Refactor these to group the logic together later,
    # just get some demo working for now
    @commands.command(
        name='image',
        help="Find an image matching the prompt."
    )
    async def find_image_legacy_format(self, context: Context, *, prompt: str = ""):
        if prompt == "":
            await context.send(ImageSearchCog.MISSING_PROMPT_MESSAGE)
            return
        await context.typing()
        image_url = None
        try:
            image_url = await asyncio.wait_for(self.fetch_image(prompt), timeout=ImageSearchCog.TIMEOUT_LIMIT)
        except asyncio.TimeoutError:
            await context.send(ImageSearchCog.TIMEOUT_ERROR_MESSAGE)
            return
        if image_url is None:
            await context.send(ImageSearchCog.SEARCH_ERROR_MESSAGE)
            return
        await context.send(image_url)

    @app_commands.command(
        name='image',
        description="Find an image matching the prompt."
    )
    @app_commands.describe(
        prompt="Search term for the image."
    )
    @app_commands.default_permissions(Permissions.all())
    async def find_image_command_format(self, interaction: Interaction, prompt: str = ""):
        if prompt == "":
            await interaction.followup.send(ImageSearchCog.MISSING_PROMPT_MESSAGE)
            return
        await interaction.response.defer(thinking=True)
        image_url = None
        try:
            image_url = await asyncio.wait_for(self.fetch_image(prompt), timeout=ImageSearchCog.TIMEOUT_LIMIT)
        except asyncio.TimeoutError:
            await interaction.followup.send(ImageSearchCog.TIMEOUT_ERROR_MESSAGE, ephemeral=True)
            return
        if image_url is None:
            await interaction.followup.send(ImageSearchCog.SEARCH_ERROR_MESSAGE, ephemeral=True)
            return
        await interaction.followup.send(image_url, ephemeral=True)

    async def fetch_image(self, prompt: str) -> str | None:
        if not self.pixabay_api_key:
            return None
        self.pixabay_api_params['q'] = prompt
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ImageSearchCog.PIXABAY_URL, params=self.pixabay_api_params) as response:
                    if response.status == 200:
                        data = await response.json()
                        hits = data.get('hits', [])
                        if hits:
                            return hits[0]['webformatURL']
            return None
        except aiohttp.ClientError:
            return None
