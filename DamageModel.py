import disnake
from abc import ABC, abstractmethod

import temporary_common_storage


class PersonNormalAttack(temporary_common_storage.AbstractPerson):
    @property
    def real_stat(self) -> int:
        return self.stat + self.buffs

    # raw damage
    @property
    def min_raw_damage(self) -> float:
        return (self.real_stat * self.weapon_atk) / 20 + self.lvl / 4

    @property
    def max_raw_damage(self) -> float:
        return (self.real_stat * self.weapon_atk) / 10 + self.lvl / 4

    @property
    def max_raw_crit_damage(self) -> float:
        return self.max_raw_damage * 1.05

    # damage
    @property
    def min_damage(self) -> float:
        return max(self.min_raw_damage - self.ctx.mob["defense"], 0)

    @property
    def max_damage(self) -> float:
        return max(self.max_raw_damage - self.ctx.mob["defense"], 0)

    @property
    def max_crit_damage(self) -> float:
        return max(self.max_raw_crit_damage - self.ctx.mob["defense"], 0)

    # accuracy and average damage
    @property
    def normal_accuracy(self) -> float:
        return max((self.max_damage / (self.max_raw_damage - self.min_raw_damage)), 0)

    @property
    def crit_accuracy(self) -> float:
        return min(1.00, (self.max_crit_damage / (self.max_raw_crit_damage - self.max_raw_damage)))

    @property
    def accuracy(self) -> float:
        return (self.normal_accuracy * 0.99) + (self.crit_accuracy * 0.01)


class PersonPowerAttack(temporary_common_storage.AbstractPerson):
    @property
    def real_stat(self) -> int:
        return self.stat + self.buffs

    # raw damage
    @property
    def min_raw_damage(self) -> float:
        if self.class_type == "magic":
            return 1.5 * (((1.08 * self.stat * self.weapon_atk) / 20) + 9 * self.lvl / 32)
        else:
            return 1.5 * (self.stat * self.weapon_atk / 20 + self.lvl / 4)

    @property
    def max_raw_damage(self) -> float:
        if self.class_type == "magic":
            return 1.5 * (((1.08 * self.stat * self.weapon_atk) / 10) + 9 * self.lvl / 32)
        else:
            return 1.5 * (self.stat * self.weapon_atk / 10 + self.lvl / 4)

    @property
    def max_raw_crit_damage(self) -> float:
        return self.max_raw_damage * 1.05

    # damage
    @property
    def min_damage(self) -> float:
        return max(self.min_raw_damage - self.ctx.mob["defense"], 0)

    @property
    def max_damage(self) -> float:
        return max(self.max_raw_damage - self.ctx.mob["defense"], 0)

    @property
    def max_crit_damage(self) -> float:
        return max(self.max_raw_crit_damage - self.ctx.mob["defense"], 0)

    # accuracy
    @property
    def normal_accuracy(self) -> float:
        return min(1.00, (self.max_damage / (self.max_raw_damage - self.min_raw_damage)))

    @property
    def crit_accuracy(self) -> float:
        return min(1.00, (self.max_crit_damage / (self.max_raw_crit_damage - self.max_raw_damage)))


class AbstractDamageModel(ABC):
    ctx: temporary_common_storage.Context

    @abstractmethod
    def __init__(self, lvl: int, stat: int, buffs: int, weapon_atk: int, class_type: str) -> None:
        ...

    @abstractmethod
    def view(self, dropdown_option: int | bool) -> disnake.Embed:
        ...


class BattleModel(AbstractDamageModel):
    def __init__(self, lvl: int, stat: int, buffs: int, weapon_atk: int, class_type: str) -> None:
        self.class_type = class_type

        self.ctx = temporary_common_storage.Context()
        self.person_normal_attack = PersonNormalAttack(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk, ctx=self.ctx, class_type=class_type)
        self.person_power_attack = PersonPowerAttack(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk, ctx=self.ctx, class_type=class_type)

    def handle_dropdown_selection(self, dropdown_option):
        if dropdown_option is False:
            return

        sorted_mobs = sorted(temporary_common_storage.mobs_info, key=lambda x: x["name"])
        for mob in sorted_mobs:
            if dropdown_option != mob["name"]:
                continue

            self.ctx.mob = mob

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
        title = f"Lvl: **{self.person_normal_attack.lvl}** {mini_slime_emoji} " \
                f"Stat: **{self.person_normal_attack.stat}** {mini_slime_emoji} " \
                f"Buffs: **{self.person_normal_attack.buffs}** {mini_slime_emoji}" \
                f"Weapon: **{self.person_normal_attack.weapon_atk} Atk **"

        # description
        description = list()

        if self.ctx.mob == self.ctx.DEFAULT_MOB:
            description.append("Select a mob")

            return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author)

        mob_name_and_emoji = f"**{self.ctx.mob['name']}** {self.ctx.mob['emoji']}"

        description.append(f"Mob: {mob_name_and_emoji}")
        description.append("")

        # простая атака
        description.append(f"Normal {class_type_and_emoji} attack:")
        if self.person_normal_attack.normal_accuracy > 0:
            description.append(f"Min. damage: **{int(self.person_normal_attack.min_damage)}**")
            description.append(f"Max. damage: **{int(self.person_normal_attack.max_damage)}**")
        elif self.person_normal_attack.normal_accuracy == 0:
            description.append("You aren't strong enough to deal normal damage to this mob.")

        if self.person_normal_attack.crit_accuracy > 0:
            description.append(f"Max. crit. damage: **{int(self.person_normal_attack.max_crit_damage)}**\n")
        elif self.person_normal_attack.crit_accuracy == 0:
            description.append("You aren't strong enough to deal critical damage to this mob. \n")

        # ульта
        description.append(f"Ultimate {class_type_and_emoji} attack:")
        if self.person_power_attack.normal_accuracy > 0:
            description.append(f"Min. ult. damage: **{int(self.person_power_attack.min_damage)}**")
            description.append(f"Max. ult. damage: **{int(self.person_power_attack.max_damage)}**")
        elif self.person_power_attack.normal_accuracy == 0:
            description.append("You aren't strong enough to deal normal damage to this mob.")

        if self.person_power_attack.crit_accuracy > 0:
            description.append(f"Max. ult. crit. damage: **{int(self.person_power_attack.max_crit_damage)}**\n")
        elif self.person_power_attack.crit_accuracy == 0:
            description.append("You aren't strong enough to deal critical damage to this mob.")

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author)
