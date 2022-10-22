from __future__ import annotations
import asyncio
from asyncio import Task
from httpx import AsyncClient, Response

from dataclasses import dataclass

from constants import BASE_API_POKEMON


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


async def httpx_fetch(url: str, client: AsyncClient) -> Response:
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


    @staticmethod
    async def fetch_pokemons(names: list[str]) -> list[Pokemon]:
        async with AsyncClient() as client:
            tasks: list[Task] = []
            for name in names:
                task: Task = asyncio.create_task(httpx_fetch(f"{BASE_API_POKEMON}{name}", client))
                tasks.append(task)
            responses: list[Response] = await asyncio.gather(*tasks)
            return [Pokemon.from_api_dict(res.json()) for res in responses]


    def __repr__(self) -> str:
        return f"{self.name=}, {self.stats}"



pokemon_names = ["bulbasaur", "pikachu", "charmander"]
pokemons = asyncio.run(Pokemon.fetch_pokemons(pokemon_names))
print(pokemons)
