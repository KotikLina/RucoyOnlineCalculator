import disnake
from abc import ABC, abstractmethod

import temporary_common_storage


class Person(temporary_common_storage.AbstractPerson):
    @property
    def lvl_experience(self) -> int:
        return int(self.lvl ** ((self.lvl / 1000) + 3))

    @property
    def experience_for_next_lvl(self) -> int:
        return int((self.lvl + 1) ** (((self.lvl + 1) / 1000) + 3))

    # mp и hp
    @property
    def hp(self) -> int:
        return 100 + self.lvl * 15

    @property
    def mp(self) -> int:
        return 100 + self.lvl * 10


class AbstractIndicatorsModel(ABC):
    @abstractmethod
    def __init__(self, lvl: int) -> None:
        ...

    @abstractmethod
    def view(self) -> disnake.Embed:
        ...


def points(numbers: int) -> str:
    if numbers // 1000000:
        return f"{f'{numbers:,}'.replace(',', '.')}"
    else:
        print("что-то тат не так...")
        return "ERROR"


class IndicatorsModel(AbstractIndicatorsModel):
    def __init__(self, lvl: int) -> None:
        self.lvl = lvl

        self.person = Person(lvl=lvl)

    # Сколько нужно для получения черепа
    @property
    def coins_required_for_while_skull(self) -> str:
        if (self.lvl * 150) // 1000000:
            return points(self.lvl * 150)
        else:
            return f'{self.lvl * 150}'

    @property
    def coins_required_for_yellow_skull(self) -> str:
        if (self.lvl * 150) // 1000000:
            return points(self.lvl * 150)
        else:
            return f'{self.lvl * 150}'

    @property
    def coins_required_for_orange_skull(self) -> str:
        if (self.lvl * 600) // 1000000:
            return points(self.lvl * 600)
        else:
            return f'{self.lvl * 600}'

    @property
    def coins_required_for_red_skull(self) -> str:
        if (self.lvl * 1950) // 1000000:
            return points(self.lvl * 1950)
        else:
            return f'{self.lvl * 1950}'

    @property
    def coins_required_for_black_skull(self) -> str:
        if (self.lvl * 6000) // 1000000:
            return points(self.lvl * 6000)
        else:
            return f'{self.lvl * 6000}'

    # Сколько потеряешь денег при смерти
    @property
    def coins_lost_by_white_skull(self) -> str:
        if (self.lvl * 50) // 1000000:
            return points(self.lvl * 50)
        else:
            return f'{self.lvl * 50}'

    @property
    def coins_lost_by_yellow_skull(self) -> str:
        if (self.lvl * 150) // 1000000:
            return points(self.lvl * 150)
        else:
            return f'{self.lvl * 150}'

    @property
    def coins_lost_by_orange_skull(self) -> str:
        if (self.lvl * 450) // 1000000:
            return points(self.lvl * 450)
        else:
            return f'{self.lvl * 450}'

    @property
    def coins_lost_by_red_skull(self) -> str:
        if (self.lvl * 1350) // 1000000:
            return points(self.lvl * 1350)
        else:
            return f'{self.lvl * 1350}'

    @property
    def coins_lost_by_black_skull(self) -> str:
        if (self.lvl * 4050) // 1000000:
            return points(self.lvl * 4050)
        else:
            return f'{self.lvl * 4050}'

    def view(self) -> disnake.Embed:
        mini_slime_emoji = "<:mini_slime:1194708281319510017>"

        white_skull = "<:white_skull:1263440267047079999>"
        yellow_skull = "<:yellow_skull:1263440802168832030>"
        orange_skull = "<:orange_skull:1263442085596364853>"
        red_skull = "<:red_skull:1263446615990206516>"
        black_skull = "<:black_skull:1263447621478125580>"

        money = "<a:money:1264709845160955905>"

        title = f"lvl: {self.lvl}  {mini_slime_emoji}  hp: {self.person.hp}  {mini_slime_emoji}  mp: {self.person.mp}"

        description = list()

        description.append(f"Base lvl: {self.lvl}  {mini_slime_emoji}  Next lvl: {self.lvl + 1}")
        description.append(f"`{points(self.person.lvl_experience)}`/`{points(self.person.experience_for_next_lvl)}` exp")
        if (self.person.experience_for_next_lvl - self.person.lvl_experience) // 1000000:
            description.append(f"You need `{f'{self.person.experience_for_next_lvl - self.person.lvl_experience:,}'.replace(',', '.')}` exp to reach `{self.lvl + 1}` lvl")
        else:
            description.append(f"You need `{self.person.experience_for_next_lvl - self.person.lvl_experience}` exp to reach `{self.lvl + 1}` lvl")

        description.append("")

        description.append(f"Золото, необходимое для получения {white_skull} черепа: `{self.coins_required_for_while_skull}` {money}")
        description.append(f"Золото, что будет потеряно при смерти с {white_skull} черепом: `{self.coins_lost_by_white_skull}` {money}")

        description.append("")

        description.append(f"Золото, необходимое для получения {yellow_skull} черепа: `{self.coins_required_for_yellow_skull}` {money}")
        description.append(f"Золото, что будет потеряно при смерти с {yellow_skull} черепом: `{self.coins_lost_by_yellow_skull}` {money}")

        description.append("")

        description.append(f"Золото, необходимое для получения {orange_skull} черепа: `{self.coins_required_for_orange_skull}` {money}")
        description.append(f"Золото, что будет потеряно при смерти с {orange_skull} черепом: `{self.coins_lost_by_orange_skull}` {money}")

        description.append("")

        description.append(f"Золото, необходимое для получения {red_skull} черепа: `{self.coins_required_for_red_skull}` {money}")
        description.append(f"Золото, что будет потеряно при смерти с {red_skull} черепом: `{self.coins_lost_by_red_skull}` {money}")

        description.append("")

        description.append(f"Золото, необходимое для получения {black_skull} черепа: `{self.coins_required_for_black_skull}` {money}")
        description.append(f"Золото, что будет потеряно при смерти с {black_skull} черепом: `{self.coins_lost_by_black_skull}` {money}")

        set_author = "Indicators"
        return disnake.Embed(title=title, description="\n".join(description)).set_author(name=set_author)
