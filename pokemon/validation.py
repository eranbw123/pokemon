from __future__ import annotations
from functools import wraps
from typing import Callable, TYPE_CHECKING

from exceptions import DuplicatePokemon, MaxPokemons
from constants import MAX_POKEMONS

if TYPE_CHECKING:
    from coche import Coach


def add_pokemons_validator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(coach: Coach, names: list[str]):
        duplicates = [
            pokemon.name for pokemon in coach.pokemons if pokemon.name in names
        ]
        if duplicates:
            raise DuplicatePokemon(duplicates)

        if (future_amount := (len(coach.pokemons) + len(names))) > MAX_POKEMONS:
            raise MaxPokemons(len(coach.pokemons), future_amount, MAX_POKEMONS)

        return func(coach, names)

    return wrapper
