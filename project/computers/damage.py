import disnake
import logging

from project.computers.abc import AbstractDamage
from project.temporary_common_storage import mobs_info
from project.structures import Person


logger = logging.getLogger(__name__)


class BattleModel(AbstractDamage):
    def __init__(self,
                 person: Person) -> None:

        self.person = person
        self.class_type = self.person.class_type

    def handle_dropdown_selection(self, dropdown_option):
        if dropdown_option is False:
            return

        sorted_mobs = sorted(mobs_info, key=lambda x: x["name"])
        for mob in sorted_mobs:
            if dropdown_option != mob["name"]:
                continue

            self.person.ctx.mob = mob

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
        set_author = "Damage Calculation"
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

        description.append(f"Mob: {mob_name_and_emoji}")
        description.append("")

        # простая атака
        description.append(f"Normal {class_type_and_emoji} attack:")
        if self.person.normal_accuracy > 0:
            description.append(f"Min. damage: **{int(self.person.min_damage)}**")
            description.append(f"Max. damage: **{int(self.person.max_damage)}**")
        elif self.person.normal_accuracy == 0:
            description.append("You aren't strong enough to deal normal damage to this mob.")

        if self.person.crit_accuracy > 0:
            description.append(f"Max. crit. damage: **{int(self.person.max_crit_damage)}**\n")
        elif self.person.crit_accuracy == 0:
            description.append("You aren't strong enough to deal critical damage to this mob. \n")

        # ульта
        description.append(f"Ultimate {class_type_and_emoji} attack:")
        if self.person.normal_accuracy_from_power_damage > 0:
            description.append(f"Min. ult. damage: **{int(self.person.min_power_damage)}**")
            description.append(f"Max. ult. damage: **{int(self.person.max_power_damage)}**")
        elif self.person.normal_accuracy_from_power_damage == 0:
            description.append("You aren't strong enough to deal normal damage to this mob.")

        if self.person.crit_accuracy_from_power_damage > 0:
            description.append(f"Max. ult. crit. damage: **{int(self.person.max_crit_power_damage)}**\n")
        elif self.person.crit_accuracy_from_power_damage == 0:
            description.append("You aren't strong enough to deal critical damage to this mob.")

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author).set_footer(text="If there is an inaccuracy - write kotiklinok#0000", icon_url="https://cdn.discordapp.com/emojis/1194708281319510017.webp")
