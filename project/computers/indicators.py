import disnake
import logging
from typing import AsyncGenerator

from project.computers.abc import AbstractIndicators


logger = logging.getLogger(__name__)


class IndicatorsModel(AbstractIndicators):
    def __init__(self, lvl: int) -> None:
        self.lvl = lvl

    @property
    def lvl_experience(self) -> int:
        return int(self.lvl ** ((self.lvl / 1000) + 3))

    @property
    def experience_for_next_lvl(self) -> int:
        return int((self.lvl + 1) ** (((self.lvl + 1) / 1000) + 3))

    async def skull_description(self, skull_info) -> AsyncGenerator[dict, None]:
        for skull, nt_coins_required_for_skull, nt_coins_lost_by_skull in skull_info:
            coins_required_for_skull = self.lvl * nt_coins_required_for_skull
            coins_lost_by_skull = self.lvl * nt_coins_lost_by_skull

            yield skull, coins_required_for_skull, coins_lost_by_skull

    async def view(self) -> disnake.Embed:
        mini_slime_emoji = "<:mini_slime:1194708281319510017>"
        money = "<a:money:1264709845160955905>"

        skull_info = [
            ["<:white_skull:1263440267047079999>", 150, 50],
            ["<:yellow_skull:1263440802168832030>", 150, 150],
            ["<:orange_skull:1263442085596364853>", 600, 450],
            ["<:red_skull:1263446615990206516>", 1950, 1350],
            ["<:black_skull:1263447621478125580>", 6000, 4050]
        ]

        title = f"lvl: {self.lvl}  {mini_slime_emoji}  hp: {100 + self.lvl * 15}  {mini_slime_emoji}  mp: {100 + self.lvl * 10}"

        description = list()

        description.append(f"Base lvl: {self.lvl}  {mini_slime_emoji}  Next lvl: {self.lvl + 1}")
        description.append(f"`{self.lvl_experience}`/`{self.experience_for_next_lvl}` exp")
        description.append(f"You need `{self.experience_for_next_lvl - self.lvl_experience}` exp to reach `{self.lvl + 1}` lvl")

        async for skull, coins_required_for_skull, coins_lost_by_skull in self.skull_description(skull_info):
            description.append("")
            description.append(f"Gold needed to obtain a {skull} skull: `{coins_required_for_skull}` {money}")
            description.append(f"Gold that will be lost on death with {skull} skull: `{coins_lost_by_skull}` {money}")

        set_author = "Indicators"
        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
