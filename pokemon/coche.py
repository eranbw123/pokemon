import asyncio

from validation import add_pokemons_validator
from pokemons import Pokemon


class Coach:
    def __init__(self, name: str, pokemons: list[str]) -> None:
        self.name = name
        self.pokemons = asyncio.run(Pokemon.fetch_pokemons(list(set(pokemons))))

    @add_pokemons_validator
    def add_pokemons(self, pokemons: list[str]):
        self.pokemons.extend(asyncio.run(Pokemon.fetch_pokemons(pokemons)))

    def __repr__(self) -> str:
        return f"{self.name=}, {self.pokemons}"
