import json
from abc import ABC
from typing import Final

with open("Mobs_info.json", "r") as file:
    data = json.load(file)

mobs_info: list[dict] = data["mobs"]
low_hp_mobs = []
high_hp_mobs = []

for mob in mobs_info:
    if mob["health"] < 10000:
        low_hp_mobs.append(mob)
    else:
        high_hp_mobs.append(mob)


class Context:
    DEFAULT_MOB: Final[dict] = {"defense": 1000}

    mob: dict

    def __init__(self, mob: dict | None = None) -> None:
        if mob is None:
            self.mob = self.DEFAULT_MOB
        else:
            self.mob = mob


class AbstractPerson(ABC):
    lvl: int
    stat: int
    buffs: int
    real_stat: int
    weapon_atk: int

    min_raw_damage: float
    max_raw_damage: float
    max_raw_crit_damage: float

    min_damage: float
    max_damage: float
    max_crit_damage: float

    normal_accuracy: int
    crit_accuracy: int
    accuracy: float

    average_damage: int

    ctx: Context

    def __init__(self, lvl: int, stat: int, buffs: int, weapon_atk: int, ctx: Context) -> None:
        self.lvl = lvl
        self.stat = stat
        self.buffs = buffs
        self.weapon_atk = weapon_atk
        self.ctx = ctx


class Person(AbstractPerson):
    @property
    def real_stat(self) -> int:
        return self.stat + self.buffs

# Train
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

    # average damage
    @property
    def average_damage(self) -> float:
        return self.accuracy * (0.99 * ((self.max_damage + self.min_damage) / 2)) + 0.01 * ((self.max_crit_damage + self.max_damage) / 2)

    # copy
    def copy(self, ctx):
        return Person(self.lvl, self.stat, self.buffs, self.weapon_atk, ctx)
