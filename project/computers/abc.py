from abc import ABC, abstractmethod

import disnake

from project.temporary_common_storage import Context
from project.structures import Person


class AbstractTrain(ABC):
    person: Person
    trained_person: Person | None
    trained_stat: int | None

    frontier_group: dict | None

    tickrate: int
    time: int

    ctx: Context

    @abstractmethod
    def __init__(self,
                 person: Person) -> None:
        ...

    @abstractmethod
    def view(self, button) -> disnake.Embed:
        ...


class AbstractPowerTrain(ABC):
    person: Person

    frontier_group: dict | None

    ctx: Context

    @abstractmethod
    def __init__(self,
                 person: Person,
                 tick: int) -> None:
        ...

    @abstractmethod
    def view(self, button) -> disnake.Embed:
        ...


class AbstractDamage(ABC):
    person: Person
    ctx: Context

    @abstractmethod
    def __init__(self,
                 person: Person,
                 tick: int) -> None:
        ...

    @abstractmethod
    def view(self, dropdown_option: int | bool) -> disnake.Embed:
        ...


class AbstractOneshot(ABC):
    ctx: Context

    @abstractmethod
    def __init__(self,
                 person: Person,
                 consistency_need: int) -> None:
        ...

    @abstractmethod
    def view(self, dropdown_option: int | bool) -> disnake.Embed:
        ...


class AbstractOffline(ABC):
    @abstractmethod
    def __init__(self,
                 current_stat: int,
                 target_stat: int = 0,
                 hours: int = 0) -> None:
        ...

    @abstractmethod
    def view(self) -> disnake.Embed:
        ...


class AbstractIndicators(ABC):
    @abstractmethod
    def __init__(self, lvl: int) -> None:
        ...

    @abstractmethod
    def view(self) -> disnake.Embed:
        ...
