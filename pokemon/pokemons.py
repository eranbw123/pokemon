from __future__ import annotations
import asyncio
from asyncio import Task
from httpx import AsyncClient, Response
from dataclasses import dataclass


from constants import BASE_API_POKEMON
from exceptions import InvalidPokemonData, PokemonFetchFalied, InvalidPokemonName
from utils import async_client_fetch


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
        try:
            return cls(*[stat["base_stat"] for stat in dict])
        except:
            raise InvalidPokemonData


class Pokemon:
    def __init__(self, name: str, id: int, types: list[str], stats: Stats) -> None:
        self.name = name
        self.id = id
        self.types = types
        self.stats = stats

    @classmethod
    def from_api_dict(cls, dict: dict) -> Pokemon:
        try:
            types = [t["type"]["name"] for t in dict["types"]]
            stats = Stats.from_api_dict(dict["stats"])
            return cls(dict["name"], dict["id"], types, stats)
        except Exception:
            raise InvalidPokemonData

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

            for res, name in zip(responses, names):
                if res.status_code == 404:
                    raise InvalidPokemonName(name)
                if status := res.status_code != 200:
                    raise PokemonFetchFalied(status)

            return [cls.from_api_dict(res.json()) for res in responses]

    def __repr__(self) -> str:
        return f"{self.name=}, {self.stats.hp=}, {self.stats.attack=}"
