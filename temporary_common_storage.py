import json

from abc import ABC
from typing import Final


with open("mobs_info.json", "r") as file:
    data = json.load(file)

mobs_info: list[dict] = data["mobs"]
mobs_melee = []

low_hp_mobs = []
high_hp_mobs = []

low_hp_melee_mobs = []
high_hp_melee_mobs = []

for mob in mobs_info:
    if mob["class_type"] == "melee":
        mobs_melee.append(mob)

    if mob["health"] < 10000:
        low_hp_mobs.append(mob)
        if mob["class_type"] == "melee":
            low_hp_melee_mobs.append(mob)
    else:
        high_hp_mobs.append(mob)
        if mob["class_type"] == "melee":
            high_hp_melee_mobs.append(mob)


with open("mob_groups.json", "r") as file:
    data = json.load(file)

mobs_groups = data


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

    hp: int
    mp: int

    lvl_experience: int
    experience_for_next_lvl: int

    class_type: str

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

    def __init__(self, ctx: Context = None, lvl: int = 0, stat: int = 0, buffs: int = 0, weapon_atk: int = 0, class_type: str = None) -> None:
        self.lvl = lvl
        self.stat = stat
        self.buffs = buffs
        self.weapon_atk = weapon_atk
        self.class_type = class_type

        self.ctx = ctx
