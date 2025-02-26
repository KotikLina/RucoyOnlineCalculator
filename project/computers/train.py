import disnake
import logging
import itertools

from typing import Final, AsyncGenerator


from project.computers.abc import AbstractTrain
from project.temporary_common_storage import Context, low_hp_mobs, mobs_info
from project.structures import Person

logger = logging.getLogger(__name__)


class BattleModel(AbstractTrain):
    REQUIRED_ACCURACY: Final[float] = 0.1749
    TRAIN_TICKRATE: Final[int] = 3600

    def __init__(self,
                 person: Person) -> None:

        self.person = person

        self.trained_person = None
        self.trained_stat = None
        self.end_game = None

    # tickrate and time
    @property
    def tickrate(self) -> int:
        return int(self.TRAIN_TICKRATE * (1.0 - (1.0 - self.person.accuracy) ** 10))

    @property
    def time(self) -> float:
        return self.person.ctx.mob['health'] / self.person.average_damage

    # Основной процесс
    async def process_mobs(self) -> AsyncGenerator[dict, None]:
        self.frontier_group = None

        key = lambda x: (x["defense"])
        iterator = itertools.groupby(sorted(low_hp_mobs, key=key, reverse=True), key=key)

        prev = None
        for _, group in iterator:
            group = tuple(group)
            self.person.ctx.mob = group[0]
            if self.person.accuracy < self.REQUIRED_ACCURACY:
                prev = group
            else:
                self.frontier_group = prev
                break

        self.end_game = False
        if 500 < group[0]["defense"]:
            self.end_game = True

        for mob in group:
            if self.person.max_damage != 0:
                yield mob
            else:
                break

    # Процесс со следующим мобом
    async def process_next_mobs(self) -> AsyncGenerator[dict, None]:
        if self.frontier_group is None:
            self.trained_person = None
            self.trained_stat = 0
            return

        ctx = Context()
        ctx.mob = self.frontier_group[0]
        self.trained_person = self.person.copy(ctx)
        self.trained_stat = 0

        while self.trained_person.accuracy < self.REQUIRED_ACCURACY:
            self.trained_person.stat += 1
            self.trained_stat += 1
        for ctx.mob in self.frontier_group:
            yield ctx.mob

    # Процесс по нажатию кнопки
    async def process_button(self, button):
        if button is False:
            return

        key = lambda x: (x["defense"])
        iterator = itertools.groupby(sorted(mobs_info, key=key, reverse=True), key=key)

        for defense, group in iterator:
            group = tuple(group)

            if defense != int(button):
                continue

            self.person.ctx.mob = group[0]
            if self.person.max_damage != 0:
                for mob in group:
                    self.person.ctx.mob = mob
                    yield mob

    async def view(self, button: int | bool) -> disnake.Embed:
        mini_slime_emoji = "<:mini_slime:1194708281319510017>"

        description = list()
        names = list()
        ttks = list()

        names_mob_button = list()
        ttks_mob_button = list()

        names_next_mob = list()

        # mob
        async for mob in self.process_mobs():
            names.append(f"{mob['name']} {mob['emoji']}")

            mins, secs = divmod(self.time, 60)
            ttks.append(f"Average time to kill {mob['name']} {mob['emoji']}: {int(mins)} min. {int(secs)} sec.")

        if self.person.max_damage != 0:
            description.append(f"You can train effectively on " + ", ".join(names))
            description.append("\n".join(ttks))
            description.append(f"Max. Damage: {int(self.person.max_damage)} {mini_slime_emoji} Tickrate: {self.tickrate} / 3600")
        else:
            description.append(f"Training is impossible. Please contact @kotiklinok with this error")

        # button
        self.person.ctx.mob = self.person.ctx.DEFAULT_MOB
        async for mob in self.process_button(button):
            names_mob_button.append(f"{mob['name']} {mob['emoji']}")

            mins_button, secs_button = divmod(self.time, 60)
            ttks_mob_button.append(f"Average time to kill {mob['name']} {mob['emoji']}: {int(mins_button)} min. {int(secs_button)} sec.")

        if self.person.max_damage != 0:
            description.append("")
            description.append(f"More information about the training on " + ", ".join(names_mob_button))
            description.append("\n".join(ttks_mob_button))
            description.append(f"Max. Damage: {int(self.person.max_damage)} {mini_slime_emoji} Tickrate: {self.tickrate} / 3600")
        elif button:
            description.append("")
            description.append("Additional training is not possible.")

        # next mob
        async for mob in self.process_next_mobs():
            names_next_mob.append(f"{mob['name']} {mob['emoji']}")

        if self.trained_person is not None:
            if self.trained_person.max_damage >= 1:
                description.append("")
                description.append(f"You can deal **{int(self.trained_person.max_damage)}** max damage to " + ", ".join(names_next_mob))
                description.append(f"You need **{self.trained_stat}** stats to train effectively on " + ", ".join(names_next_mob))
            else:
                description.append("")
                description.append(f"You cant deal damage to " + ", ".join(names_next_mob))
                description.append(f"You need **{self.trained_stat}** stats to train effectively on " + ", ".join(names_next_mob))

        set_author = "Training Calculation"

        title = f"Lvl: **{self.person.lvl}** {mini_slime_emoji} " \
                f"Stat: **{self.person.stat}** {mini_slime_emoji} " \
                f"Buffs: **{self.person.buffs}** {mini_slime_emoji}" \
                f"Weapon: **{self.person.weapon_atk} Atk **"

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
