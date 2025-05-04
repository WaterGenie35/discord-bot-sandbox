import asyncio
from typing import List

import feedparser
from feedparser import FeedParserDict

from discord import Embed
from discord import TextChannel
from discord import ChannelType
from discord.ext.commands import Bot
from discord.ext.commands import Cog


class MonitorRSSCog(Cog):
    
    FEED_URL = 'https://lorem-rss.herokuapp.com/feed'
    OUTPUT_CHANNEL_NAME = "rss-feed"
    
    def __init__(self, bot: Bot):
        self.bot_client = bot
        self.last_etag = None
        self.last_published = None
        self.channels = self.get_broadcast_channels()
        self.tracking_task = asyncio.create_task(self.track_rss_feed())
        
        print("Initialized rss cog.")
    
    def get_broadcast_channels(self) -> List[TextChannel]:
        channels = []
        for guild in self.bot_client.guilds:
            text_channels = [
                channel for channel in guild.channels
                if channel.type == ChannelType.text and channel.name == MonitorRSSCog.OUTPUT_CHANNEL_NAME
            ]
            channels.extend(text_channels)
        return channels

    async def track_rss_feed(self):
        while True:
            await asyncio.sleep(300)
            embeds = await self.get_new_entries()
            for channel in self.channels:
                for embed in embeds:
                    await channel.send(embed=embed)
    
    # Also 
    async def get_new_entries(self) -> List[Embed]:
        feed: FeedParserDict | None = None
        if self.last_etag is not None:
            feed = feedparser.parse(MonitorRSSCog.FEED_URL, etag=self.last_etag)
        else:
            feed = feedparser.parse(MonitorRSSCog.FEED_URL)
        if feed is None:
            return []
        self.last_etag = feed.etag
        
        embeds = []
        for entry in reversed(feed.entries):
            if self.last_published is not None and entry.published_parsed < self.last_published:
                continue
            entry_embed = Embed(
                title=entry.title,
                description=entry.summary,
                url=entry.link
            )
            entry_embed.set_footer(text=f"{entry.author} • Published {entry.published}")
            embeds.append(entry_embed)
        if len(embeds) > 0:
            self.last_published = feed.entries[0].published_parsed

        return embeds
