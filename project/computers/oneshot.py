import disnake
import logging

from project.computers.abc import AbstractOneshot
from project.temporary_common_storage import mobs_info
from project.structures import Person

logger = logging.getLogger(__name__)


class OneshotModel(AbstractOneshot):
    def __init__(self,
                 person: Person,
                 consistency_need: int) -> None:

        self.person = person
        self.class_type = self.person.class_type

        self.consistency_need = None
        if consistency_need:
            self.consistency_need = consistency_need
        self.trained_person = None
        self.trained_stat = None

    def handle_dropdown_selection(self, dropdown_option):
        if dropdown_option is False:
            return

        sorted_mobs = sorted(mobs_info, key=lambda x: x["name"])
        for mob in sorted_mobs:
            if dropdown_option != mob["name"]:
                continue

            self.person.ctx.mob = mob

    async def process(self, person):
        self.trained_person = person.copy(ctx=self.person.ctx)
        self.trained_stat = 0

        while self.trained_person.consistency_from_power_damage * 100 < self.consistency_need:
            self.trained_person.stat += 1
            self.trained_stat += 1

        trained_stat_with_power_damage = self.trained_stat

        while self.trained_person.consistency * 100 < self.consistency_need:
            self.trained_person.stat += 1
            self.trained_stat += 1

        trained_stat_with_damage = self.trained_stat

        return f"{trained_stat_with_power_damage}", f"{trained_stat_with_damage}"

    async def view(self, dropdown_option) -> disnake.Embed:
        mini_slime_emoji = "<:mini_slime:1194708281319510017>"

        if dropdown_option:
            self.handle_dropdown_selection(dropdown_option=dropdown_option)

        class_type_and_emoji = ""
        if self.class_type == "melee":
            class_type_and_emoji = "Melee :crossed_swords:"

        if self.class_type == "distance":
            class_type_and_emoji = "Distance :bow_and_arrow:"

        if self.class_type == "magic":
            class_type_and_emoji = "Magic :fire:"

        # author and title
        set_author = "Oneshot Calculation"
        title = f"Lvl: **{self.person.lvl}** {mini_slime_emoji} " \
                f"Stat: **{self.person.stat}** {mini_slime_emoji} " \
                f"Buffs: **{self.person.buffs}** {mini_slime_emoji}" \
                f"Weapon: **{self.person.weapon_atk} Atk **"

        # description
        description = list()

        if self.person.ctx.mob == self.person.ctx.DEFAULT_MOB:
            description.append("Select a mob")

            return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author)

        mob_name_and_emoji = f"**{self.person.ctx.mob['name']}** {self.person.ctx.mob['emoji']}"

        process_power_person, process_normal_person = await self.process(self.person)

        description.append(f"Mob: {mob_name_and_emoji}")
        description.append("")

        # простая атака
        description.append(f"{class_type_and_emoji} normal damage:")
        if self.person.normal_accuracy > 0:
            description.append(
                f"Min. damage: **{int(self.person.min_damage)}**  {mini_slime_emoji}  Max. damage: **{int(self.person.max_damage)}**  {mini_slime_emoji}  Max. crit. damage: **{int(self.person.max_crit_damage)}**")
        elif self.person.crit_accuracy > 0:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"Max. crit. damage: **{int(self.person.max_crit_damage)}**")
        else:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"You aren't strong enough to deal critical damage to this mob!")

        if self.person.consistency > 0:
            description.append(
                f"You **can** already one-shot a {mob_name_and_emoji} with auto attack at {min(int(self.person.consistency * 100), 100)}% consistency")
        else:
            description.append(f"You **cannot** one-shot a {mob_name_and_emoji} with auto attack yet")

        if self.person.consistency * 100 < self.consistency_need:
            description.append(
                f"You need **{process_normal_person}** stat to one-shot a {mob_name_and_emoji} with **{self.consistency_need}%** consistency")
        description.append("")

        # ульта
        description.append(f"{class_type_and_emoji} ultimate damage:")
        if self.person.normal_accuracy_from_power_damage > 0:
            description.append(
                f"Min. damage: **{int(self.person.min_power_damage)}**  {mini_slime_emoji}  Max. damage: **{int(self.person.max_power_damage)}**  {mini_slime_emoji}  Max. crit. damage: **{int(self.person.max_crit_power_damage)}**")
        elif self.person.crit_accuracy_from_power_damage > 0:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"Max. crit. damage: **{int(self.person.max_crit_power_damage)}**")
        else:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append("You aren't strong enough to deal critical damage to this mob!")

        if self.person.consistency_from_power_damage > 0:
            description.append(
                f"You **can** already one-shot a {mob_name_and_emoji} with ultimate at {min(int(self.person.consistency_from_power_damage * 100), 100)}% consistency")
        else:
            description.append(f"You **cannot** one-shot a {mob_name_and_emoji} with ultimate yet")

        if self.person.consistency_from_power_damage * 100 < self.consistency_need:
            description.append(
                f"You need **{process_power_person}** stat to one-shot a {mob_name_and_emoji} with **{self.consistency_need}%** consistency")

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
