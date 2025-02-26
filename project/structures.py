from abc import ABC
from project.temporary_common_storage import Context


class AbstractPerson(ABC):
    lvl: int
    stat: int
    buffs: int
    real_stat: int
    weapon_atk: int

    class_type: str

    min_raw_damage: float
    max_raw_damage: float
    max_raw_crit_damage: float

    min_raw_power_damage: float
    max_raw_power_damage: float
    max_raw_crit_power_damage: float

    min_damage: float
    max_damage: float
    max_crit_damage: float

    min_power_damage: float
    max_power_damage: float
    max_crit_power_damage: float

    normal_accuracy: int
    crit_accuracy: int
    accuracy: float

    normal_accuracy_from_power_damage: int
    crit_accuracy_from_power_damage: int
    accuracy_from_power_damage: float

    average_damage: int
    average_damage_from_power_damage: int

    consistency: int
    consistency_from_power_damage: int

    ctx: Context

    def __init__(self,
                 ctx: Context = None,
                 lvl: int = 0,
                 stat: int = 0,
                 buffs: int = 0,
                 weapon_atk: int = 0,
                 class_type: str = None) -> None:
        self.lvl = lvl
        self.stat = stat
        self.buffs = buffs
        self.weapon_atk = weapon_atk
        self.class_type = class_type

        self.ctx = ctx


class Person(AbstractPerson):
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

    # raw power damage
    @property
    def min_raw_power_damage(self) -> float:
        if self.class_type == "magic":
            return 1.5 * (((1.08 * self.stat * self.weapon_atk) / 20) + 9 * self.lvl / 32)
        else:
            return 1.5 * (self.stat * self.weapon_atk / 20 + self.lvl / 4)

    @property
    def max_raw_power_damage(self) -> float:
        if self.class_type == "magic":
            return 1.5 * (((1.08 * self.stat * self.weapon_atk) / 10) + 9 * self.lvl / 32)
        else:
            return 1.5 * (self.stat * self.weapon_atk / 10 + self.lvl / 4)

    @property
    def max_raw_crit_power_damage(self) -> float:
        return self.max_raw_power_damage * 1.05

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

    # power damage
    @property
    def min_power_damage(self) -> float:
        return max(self.min_raw_power_damage - self.ctx.mob["defense"], 0)

    @property
    def max_power_damage(self) -> float:
        return max(self.max_raw_power_damage - self.ctx.mob["defense"], 0)

    @property
    def max_crit_power_damage(self) -> float:
        return max(self.max_raw_crit_power_damage - self.ctx.mob["defense"], 0)

    # accuracy
    @property
    def normal_accuracy(self) -> float:
        return max((self.max_damage / (self.max_raw_damage - self.min_raw_damage)), 0)

    @property
    def crit_accuracy(self) -> float:
        return min(1.00, (self.max_crit_damage / (self.max_raw_crit_damage - self.max_raw_damage)))

    @property
    def accuracy(self) -> float:
        return (self.normal_accuracy * 0.99) + (self.crit_accuracy * 0.01)

    # accuracy from power damage
    @property
    def normal_accuracy_from_power_damage(self) -> float:
        return min(1.00, (self.max_power_damage / (self.max_raw_power_damage - self.min_raw_power_damage)))

    @property
    def crit_accuracy_from_power_damage(self) -> float:
        return min(1.00, (self.max_crit_power_damage / (self.max_raw_crit_power_damage - self.max_raw_power_damage)))

    @property
    def accuracy_from_power_damage(self) -> float:
        return (self.normal_accuracy_from_power_damage * 0.99) + (self.crit_accuracy_from_power_damage * 0.01)

    # average damage
    @property
    def average_damage(self) -> float:
        return self.accuracy * (0.99 * ((self.max_damage + self.min_damage) / 2)) + 0.01 * ((self.max_crit_damage + self.max_damage) / 2)

    @property
    def average_damage_from_power_damage(self) -> float:
        return self.accuracy_from_power_damage * (0.99 * ((self.max_power_damage + self.min_power_damage) / 2)) + 0.01 * ((self.max_crit_power_damage + self.max_power_damage) / 2)

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

    @property
    def consistency_from_power_damage(self) -> float:
        mob_life = self.ctx.mob['health'] + self.ctx.mob["defense"]

        if mob_life - self.max_raw_crit_power_damage > 0:
            return 0

        range_atk = self.max_raw_power_damage - self.min_raw_power_damage
        normal_oneshot = self.max_raw_power_damage - mob_life
        if normal_oneshot > 0:
            normal_consistency = normal_oneshot / range_atk
            return normal_consistency * 0.99 + 0.01
        else:
            crit_range = self.max_raw_crit_power_damage - self.max_raw_power_damage
            critical_oneshot = self.max_raw_crit_power_damage - mob_life
            return (critical_oneshot / crit_range) * 0.01

    # copy
    def copy(self, ctx):
        return Person(lvl=self.lvl, stat=self.stat, buffs=self.buffs, weapon_atk=self.weapon_atk, ctx=ctx, class_type=self.class_type)
