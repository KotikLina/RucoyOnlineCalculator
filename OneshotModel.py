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

    # consistency
    @property
    def consistency(self) -> float:
        mob_life = self.ctx.mob['health'] + self.ctx.mob["defense"]

        if mob_life - self.max_raw_crit_damage > 0:
            return 0

        range_atk = self.max_raw_damage - self.min_raw_damage
        normal_oneshot = self.max_raw_damage - mob_life
        if normal_oneshot > 0:
            normal_consistency = normal_oneshot / range_atk
            return normal_consistency * 0.99 + 0.01
        else:
            crit_range = self.max_raw_crit_damage - self.max_raw_damage
            critical_oneshot = self.max_raw_crit_damage - mob_life
            return (critical_oneshot / crit_range) * 0.01

    # copy
    def copy(self, ctx):
        return PersonNormalAttack(lvl=self.lvl, stat=self.stat, buffs=self.buffs, weapon_atk=self.weapon_atk, ctx=ctx, class_type=self.class_type)


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

    # consistency
    @property
    def consistency(self) -> float:
        mob_life = self.ctx.mob['health'] + self.ctx.mob["defense"]

        if mob_life - self.max_raw_crit_damage > 0:
            return 0

        range_atk = self.max_raw_damage - self.min_raw_damage
        normal_oneshot = self.max_raw_damage - mob_life
        if normal_oneshot > 0:
            normal_consistency = normal_oneshot / range_atk
            return normal_consistency * 0.99 + 0.01
        else:
            crit_range = self.max_raw_crit_damage - self.max_raw_damage
            critical_oneshot = self.max_raw_crit_damage - mob_life
            return (critical_oneshot / crit_range) * 0.01

    # copy
    def copy(self, ctx):
        return PersonPowerAttack(lvl=self.lvl, stat=self.stat, buffs=self.buffs, weapon_atk=self.weapon_atk, ctx=ctx, class_type=self.class_type)


class AbstractOneshotModel(ABC):
    ctx: temporary_common_storage.Context

    @abstractmethod
    def __init__(self, lvl: int, stat: int, buffs: int, weapon_atk: int, class_type: str, consistency_need: int) -> None:
        ...

    @abstractmethod
    def view(self, dropdown_option: int | bool) -> disnake.Embed:
        ...


class OneshotModel(AbstractOneshotModel):
    def __init__(self, lvl: int, stat: int, buffs: int, weapon_atk: int, class_type: str, consistency_need: int) -> None:
        self.class_type = class_type

        self.ctx = temporary_common_storage.Context()
        self.person_normal_attack = PersonNormalAttack(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk, ctx=self.ctx, class_type=class_type)
        self.person_power_attack = PersonPowerAttack(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk, ctx=self.ctx, class_type=class_type)

        self.consistency_need = None
        if consistency_need:
            self.consistency_need = consistency_need
        self.trained_person = None
        self.trained_stat = None

    def handle_dropdown_selection(self, dropdown_option):
        if dropdown_option is False:
            return

        sorted_mobs = sorted(temporary_common_storage.mobs_info, key=lambda x: x["name"])
        for mob in sorted_mobs:
            if dropdown_option != mob["name"]:
                continue

            self.ctx.mob = mob

    async def process(self, person):
        self.trained_person = person.copy(ctx=self.ctx)
        self.trained_stat = 0

        while self.trained_person.consistency * 100 < self.consistency_need:
            self.trained_person.stat += 1
            self.trained_stat += 1

        return f"{self.trained_stat}"

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

        process_normal_person = await self.process(self.person_normal_attack)
        process_power_person = await self.process(self.person_power_attack)

        description.append(f"Mob: {mob_name_and_emoji}")
        description.append("")

        # простая атака
        description.append(f"{class_type_and_emoji} normal damage:")
        if self.person_normal_attack.normal_accuracy > 0:
            description.append(f"Min. damage: **{int(self.person_normal_attack.min_damage)}**  {mini_slime_emoji}  Max. damage: **{int(self.person_normal_attack.max_damage)}**  {mini_slime_emoji}  Max. crit. damage: **{int(self.person_normal_attack.max_crit_damage)}**")
        elif self.person_normal_attack.crit_accuracy > 0:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"Max. crit. damage: **{int(self.person_normal_attack.max_crit_damage)}**")
        else:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"You aren't strong enough to deal critical damage to this mob!")

        if self.person_normal_attack.consistency > 0:
            description.append(f"You **can** already one-shot a {mob_name_and_emoji} with auto attack at {min(int(self.person_normal_attack.consistency * 100), 100)}% consistency")
        else:
            description.append(f"You **cannot** one-shot a {mob_name_and_emoji} with auto attack yet")

        if self.person_normal_attack.consistency * 100 < self.consistency_need:
            description.append(f"You need **{process_normal_person}** stat to one-shot a {mob_name_and_emoji} with **{self.consistency_need}%** consistency")
        description.append("")

        # ульта
        description.append(f"{class_type_and_emoji} ultimate damage:")
        if self.person_power_attack.normal_accuracy > 0:
            description.append(f"Min. damage: **{int(self.person_power_attack.min_damage)}**  {mini_slime_emoji}  Max. damage: **{int(self.person_power_attack.max_damage)}**  {mini_slime_emoji}  Max. crit. damage: **{int(self.person_power_attack.max_crit_damage)}**")
        elif self.person_power_attack.crit_accuracy > 0:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append(f"Max. crit. damage: **{int(self.person_power_attack.max_crit_damage)}**")
        else:
            description.append("You aren't strong enough to deal normal damage to this mob!")
            description.append("You aren't strong enough to deal critical damage to this mob!")

        if self.person_power_attack.consistency > 0:
            description.append(f"You **can** already one-shot a {mob_name_and_emoji} with ultimate at {min(int(self.person_power_attack.consistency * 100), 100)}% consistency")
        else:
            description.append(f"You **cannot** one-shot a {mob_name_and_emoji} with ultimate yet")

        if self.person_power_attack.consistency * 100 < self.consistency_need:
            description.append(f"You need **{process_power_person}** stat to one-shot a {mob_name_and_emoji} with **{self.consistency_need}%** consistency")

        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author)
