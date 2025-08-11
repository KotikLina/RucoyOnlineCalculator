import disnake
import logging
from typing import Optional

from project.computers.abc import AbstractOffline


logger = logging.getLogger(__name__)


class OfflineModel(AbstractOffline):
    def __init__(self,
                 current_stat: Optional[int],
                 target_stat: Optional[int] = None,
                 hours: Optional[int] = None) -> None:
        self.current_stat = current_stat
        self.target_stat = target_stat
        self.hours = hours

    @staticmethod
    def calc_ticks(x):
        if x <= 54:
            return x ** ((x / 1000) + 2.373)
        else:
            return x ** ((x / 1000) + 2.171)

    @property
    def current_stat_ticks(self) -> float:
        return self.calc_ticks(self.current_stat)

    @property
    def target_stat_ticks(self) -> float:
        return self.calc_ticks(self.target_stat)

    @property
    def ticks_in_hours(self) -> int:
        return 600 * self.hours

    @property
    def total_ticks(self) -> float:
        return self.ticks_in_hours + self.current_stat_ticks

    @property
    def found_stat(self) -> float:
        for stat in range(5, 1000):
            if self.total_ticks <= self.calc_ticks(stat):
                fract = (self.total_ticks - self.calc_ticks(stat - 1)) / (self.calc_ticks(stat) - self.calc_ticks(stat - 1))
                return (stat - 1) + fract
        return 0.0

    @property
    def new_stat(self) -> float:
        return round(100.0 * self.found_stat) / 100.0

    async def view(self) -> disnake.Embed:
        mini_slime_emoji = "<:mini_slime:1194708281319510017>"

        set_author = "Offline Calculation"
        title = ""
        description = list()

        if self.target_stat is not None:
            total_ticks = self.target_stat_ticks - self.current_stat_ticks

            title = f"Current stat: {self.current_stat}  {mini_slime_emoji}  target stat: {self.target_stat}"
            description.append(
                f"You need approximately **{total_ticks:,.0f}** ticks until you reach stat level **{self.target_stat:,d}**")
            description.append(
                f"This is around **{total_ticks * 60 / 600:,.0f}** minutes, or **{total_ticks / 600:,.1f}** hours of offline training at **600** exp/hr")
        elif self.hours is not None:
            title = f"Initial Stat: **{self.current_stat:,d}** {mini_slime_emoji} Hours: **{self.hours:,d}**"
            description.append(f"Your new stat will be approximately: **{round(self.new_stat)}** with **{self.hours}** hours of offline training")

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
