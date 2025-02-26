import disnake
import logging
import itertools

from typing import AsyncGenerator

from project.computers.abc import AbstractPowerTrain
from project.temporary_common_storage import Context, low_hp_melee_mobs, mobs_melee
from project.structures import Person


logger = logging.getLogger(__name__)


class BattleModel(AbstractPowerTrain):
    def __init__(self,
                 person: Person,
                 tick: int) -> None:

        self.person = person
        self.class_type = self.person.class_type
        self.tick = tick

        self.trained_person = None
        self.trained_stat = None
        self.end_game = None

    @property
    def threshold(self) -> float:
        return 1.0 - 0.8251 ** (1.0 / self.tick)

    @property
    def total_accuracy(self) -> float:
        return 1.0 - (((1.0 - self.person.accuracy_from_power_damage) ** self.tick) ** 10)

    @property
    def max_tickrate(self) -> int:
        return self.tick * 3600 if self.tick <= 5 else 18000

    @property
    def tickrate(self) -> int:
        return int(self.max_tickrate * self.total_accuracy)

    @property
    def time(self) -> float:
        return self.person.ctx.mob['health'] / self.person.average_damage_from_power_damage

    # Основной процесс
    async def process_mobs(self) -> AsyncGenerator[dict, None]:
        self.frontier_group = None

        key = lambda x: (x["defense"])
        iterator = itertools.groupby(sorted(low_hp_melee_mobs, key=key, reverse=True), key=key)

        prev = None
        for _, group in iterator:
            group = tuple(group)
            self.person.ctx.mob = group[0]
            if self.person.accuracy_from_power_damage < self.threshold:
                prev = group
            else:
                self.frontier_group = prev
                break

        self.end_game = False
        if 500 < group[0]["defense"]:
            self.end_game = True

        for mob in group:
            if self.person.max_power_damage != 0:
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

        while self.trained_person.accuracy_from_power_damage < self.threshold:
            self.trained_person.stat += 1
            self.trained_stat += 1
        for ctx.mob in self.frontier_group:
            yield ctx.mob

    # Процесс по нажатию кнопки
    async def process_button(self, button):
        if button is False:
            return

        key = lambda x: (x["defense"])
        iterator = itertools.groupby(sorted(mobs_melee, key=key, reverse=True), key=key)

        for defense, group in iterator:
            group = tuple(group)

            if defense != int(button):
                continue

            self.person.ctx.mob = group[0]
            if self.person.max_power_damage != 0:
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

        class_type_and_emoji = ""
        if self.class_type == "melee":
            class_type_and_emoji = "Melee :crossed_swords:"

        if self.class_type == "distance":
            class_type_and_emoji = "Distance :bow_and_arrow:"

        if self.class_type == "magic":
            class_type_and_emoji = "Magic :fire:"

        # mob
        async for mob in self.process_mobs():
            names.append(f"{mob['name']} {mob['emoji']}")

            mins, secs = divmod(self.time, 60)
            ttks.append(f"Average time to kill {mob['name']} {mob['emoji']}: {int(mins)} min. {int(secs)} sec.")

        if self.person.max_power_damage != 0:
            description.append(f"You can **{class_type_and_emoji}** power train effectively on " + ", ".join(names))
            description.append("\n".join(ttks))
            description.append(f"Max. Damage: {int(self.person.max_power_damage)} {mini_slime_emoji} Tickrate: {self.tickrate} / {self.max_tickrate}")
        else:
            description.append(f"Training is impossible. Please contact @kotiklinok with this error")

        # button
        self.person.ctx.mob = self.person.ctx.DEFAULT_MOB
        async for mob in self.process_button(button):
            names_mob_button.append(f"{mob['name']} {mob['emoji']}")

            mins_button, secs_button = divmod(self.time, 60)
            ttks_mob_button.append(f"Average time to kill {mob['name']} {mob['emoji']}: {int(mins_button)} min. {int(secs_button)} sec.")

        if self.person.max_power_damage != 0:
            description.append("")
            description.append(f"More information about the **{class_type_and_emoji}** power training on " + ", ".join(names_mob_button))
            description.append("\n".join(ttks_mob_button))
            description.append(f"Max. Damage: {int(self.person.max_power_damage)} {mini_slime_emoji} Tickrate: {self.tickrate} / {self.max_tickrate}")
        elif button:
            description.append("")
            description.append("Additional training is not possible.")

        # next mob
        async for mob in self.process_next_mobs():
            names_next_mob.append(f"{mob['name']} {mob['emoji']}")

        if self.trained_person is not None:
            if self.trained_person.max_damage >= 1:
                description.append("")
                description.append(f"You can deal **{int(self.trained_person.max_power_damage)}** max damage to " + ", ".join(names_next_mob))
                description.append(f"You need **{self.trained_stat}** stats to **{class_type_and_emoji}** power train effectively on " + ", ".join(names_next_mob))
            else:
                description.append("")
                description.append(f"You cant deal damage to " + ", ".join(names_next_mob))
                description.append(f"You need **{self.trained_stat}** stats to **{class_type_and_emoji}** power train effectively on " + ", ".join(names_next_mob))

        set_author = "Power Training Calculation"
        title = f"Lvl: **{self.person.lvl}** {mini_slime_emoji} " \
                f"Stat: **{self.person.stat}** {mini_slime_emoji} " \
                f"Buffs: **{self.person.buffs}** {mini_slime_emoji}" \
                f"Weapon: **{self.person.weapon_atk} Atk ** {mini_slime_emoji}" \
                f"Tick: **{self.tick}**"

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
