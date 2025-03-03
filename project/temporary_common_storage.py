import json
from typing import Final


with open("static/data/mobs_info.json", "r") as file:
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


with open("static/data/mob_groups.json", "r") as file:
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
