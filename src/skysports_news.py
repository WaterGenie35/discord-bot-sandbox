from bs4 import BeautifulSoup
import requests

from discord import Embed
from discord import Interaction
from discord import app_commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog


# Web scraping demo
class SkySportsNewsCog(Cog):
    
    NEWS_URL = 'https://www.skysports.com/nfl'
    ARTICLE_COUNT = 3
    
    def __init__(self, bot: Bot):
        self.bot_client = bot
        
        print("Initialized Sky Sports news cog.")
    
    @app_commands.command(
        name='nflnews',
        description="Get the latest NFL news from the Sky Sports website."
    )
    async def get_latest_nfl_news(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        page = requests.get(SkySportsNewsCog.NEWS_URL)
        soup = BeautifulSoup(page.content, 'lxml')
        news_div = soup.find_all('div', class_='news-list__item',limit=SkySportsNewsCog.ARTICLE_COUNT)
        embeds = []
        for item in news_div:
            link = item.find('a')
            article_embed = Embed(
                title=item.find('h4').get_text(strip=True),
                description=item.find('p').get_text(strip=True),
                url=link['href']
            )
            article_embed.set_thumbnail(url=link.find('img')['data-src'])
            embeds.append(article_embed)
        await interaction.followup.send(embeds=embeds)
