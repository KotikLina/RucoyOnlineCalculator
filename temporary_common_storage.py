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
