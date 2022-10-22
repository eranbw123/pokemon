from __future__ import annotations
from dataclasses import dataclass
import requests

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
    def from_dict(cls, dict: dict) -> Stats:
        return cls(*[stat["base_stat"] for stat in dict])

class Pokemon:
    def __init__(self, name: str, id: int, types: list[str], stats: Stats) -> None:
        self.name = name
        self.id = id
        self.types = types
        self.stats = stats


    @classmethod
    def from_dict(cls, dict: dict) -> Pokemon:
        types = [t["type"]["name"] for t in dict["types"]]
        stats = Stats.from_dict(dict["stats"])
        return cls(dict["name"], dict["id"], types, stats)


    @classmethod
    def from_api(cls, name: str) -> Pokemon:
        res = requests.get(url=f"{BASE_API_POKEMON}{name}")
        return cls.from_dict(res.json())
        

    def __repr__(self) -> str:
        return f"{self.name=}, {self.stats}"




pokemon_name = ["bulbasaur", "pikachu", "charmander"]
pokemon = Pokemon.from_api("pikachu")
print(pokemon)