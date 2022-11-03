from __future__ import annotations
import asyncio
from asyncio import Task
from typing import Callable
from httpx import AsyncClient, Response
from dataclasses import dataclass
from functools import wraps

from constants import BASE_API_POKEMON, MAX_POKEMONS


class DuplicatePokemon(Exception):
    pass


class MaxPokemons(Exception):
    def __init__(self, current_amount: int, future_amount: int) -> None:
        super().__init__(
            f"you already have {current_amount} pokemons, if added you would have {future_amount}, which exceeds {MAX_POKEMONS}"
        )


def add_pokemons_validator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(coach: Coach, names: list[str]):
        duplicates = [
            pokemon.name for pokemon in coach.pokemons if pokemon.name in names
        ]
        if duplicates:
            raise DuplicatePokemon(duplicates)

        if (future_amount := (len(coach.pokemons) + len(names))) > MAX_POKEMONS:
            raise MaxPokemons(len(coach.pokemons), future_amount)

        return func(coach, names)

    return wrapper


def test_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        return func(*args, **kwargs)

    return wrapper


@dataclass
class Stats:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defence: int
    speed: int

    @classmethod
    def from_api_dict(cls, dict: dict) -> Stats:
        return cls(*[stat["base_stat"] for stat in dict])


async def async_client_fetch(url: str, client: AsyncClient) -> Response:
    return await client.get(url)


class Pokemon:
    def __init__(self, name: str, id: int, types: list[str], stats: Stats) -> None:
        self.name = name
        self.id = id
        self.types = types
        self.stats = stats

    @classmethod
    def from_api_dict(cls, dict: dict) -> Pokemon:
        types = [t["type"]["name"] for t in dict["types"]]
        stats = Stats.from_api_dict(dict["stats"])
        return cls(dict["name"], dict["id"], types, stats)

    @classmethod
    async def fetch_pokemons(cls, names: list[str]) -> list[Pokemon]:
        async with AsyncClient() as client:
            tasks: list[Task] = []
            for name in names:
                task: Task = asyncio.create_task(
                    async_client_fetch(f"{BASE_API_POKEMON}{name}", client)
                )
                tasks.append(task)
            responses: list[Response] = await asyncio.gather(*tasks)
            return [cls.from_api_dict(res.json()) for res in responses]

    def __repr__(self) -> str:
        return f"{self.name=}, {self.stats.hp=}, {self.stats.attack=}"


class Coach:
    def __init__(self, name: str, pokemons: list[str]) -> None:
        self.name = name
        self.pokemons = asyncio.run(Pokemon.fetch_pokemons(list(set(pokemons))))

    @add_pokemons_validator
    def add_pokemons(self, pokemons: list[str]):
        self.pokemons.extend(asyncio.run(Pokemon.fetch_pokemons(pokemons)))

    def __repr__(self) -> str:
        return f"{self.name=}, {self.pokemons}"


pokemon_names = ["bulbasaur", "pikachu", "charmander", "charmander"]
c = Coach(name="eran", pokemons=pokemon_names)
print(c)
c.add_pokemons(["ditto"])
print(c)
