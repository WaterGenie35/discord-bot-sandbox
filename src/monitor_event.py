import asyncio
import random
import math
from typing import List

from discord import TextChannel
from discord import ChannelType
from discord.ext.commands import Bot
from discord.ext.commands import Cog

from faker import Faker

class MonitorEventCog(Cog):
    def __init__(self, bot: Bot):
        self.bot_client = bot
        self.faker = Faker()
        self.channels = self.get_broadcast_channels()
        self.tracking_task = asyncio.create_task(self.track_live_data())
        
        print("Initialized subscription cog.")
    
    def get_broadcast_channels(self) -> List[TextChannel]:
        channels = []
        for guild in self.bot_client.guilds:
            text_channels = [
                channel for channel in guild.channels
                if channel.type == ChannelType.text and channel.name == "latest-updates"
            ]
            channels.extend(text_channels)
        return channels
    
    async def track_live_data(self):
        # Just posting random dummy data periodically to simulate incoming traffic
        events = [
            self.player_join_event,
            self.player_lost_event,
            self.sports_outcome_event,
            self.country_win,
            self.country_lost
        ]
        while True:
            await asyncio.sleep(random.uniform(3, 12))
            event = random.choice(events)
            for channel in self.channels:
                await channel.send(event())
    
    def player_join_event(self) -> str:
        player = self.faker.name()
        company = self.faker.company()
        amount = math.floor(random.uniform(2, 28))
        amount_text = None
        if amount < 10:
            amount_text = f"${amount}00k"
        else:
            amount_text = f"${amount}M"
        return f"{player} signed a contract with {company} for {amount_text}."
    
    def player_lost_event(self) -> str:
        player = self.faker.name()
        company = self.faker.company()
        self.faker.day_of_week()
        variations = [
            f"{player} broke off with {company} last {self.faker.day_of_week()}.",
            f"{company} let go of their star-player {player}.",
            f"{player} ended their contract with {company} from all the backlash.",
            f"{player} returned home after a devastating lost against {company} last week."
        ]
        return random.choice(variations)

    def sports_outcome_event(self) -> str:
        team_1 = self.faker.company()
        team_2 = self.faker.company()
        score_1 = math.floor(random.uniform(5, 80))
        score_2 = math.floor(random.uniform(2, score_1 - 1))
        event_name = self.faker.city()
        event_suffix = ["Cup", "League", "Regional", "Invitational", "Championship"]
        return f"{team_1} won {score_1}-{score_2} against {team_2} in the {event_name} {random.choice(event_suffix)}"

    def country_win(self) -> str:
        country = self.faker.country()
        opponent = self.faker.country()
        player = self.faker.country()
        events = [
            "European Regionals",
            "Grand Prix",
            "Olympics"
        ]
        variations = [
            f"{player} brought home the first gold medal for {country}.",
            f"{country} got their first silver medal in the {random.choice(events)}."
            f"{country} got their first win against {opponent} in {math.floor(random.uniform(4, 10))} years.",
        ]
        return random.choice(variations)

    def country_lost(self) -> str:
        country = self.faker.country()
        opponent = self.faker.country()
        player = self.faker.name()
        event_name = self.faker.city()
        event_suffix = ["Cup", "League", "Regional", "Invitational", "Championship"]
        variations = [
            f"{country} suffered a devastating lost against {opponent} in the {event_name} {random.choice(event_suffix)}",
            f"{country} lost against {opponent} for the first time after letting go of {player}"
        ]
        return random.choice(variations)
