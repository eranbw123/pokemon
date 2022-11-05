class DuplicatePokemon(Exception):
    pass


class InvalidPokemonData(Exception):
    pass


class PokemonFetchFalied(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"fetch failed with {status_code=}")


class InvalidPokemonName(Exception):
    def __init__(self, pokemon_name: str) -> None:
        super().__init__(f"{pokemon_name=} does not exist")


class MaxPokemons(Exception):
    def __init__(self, current_amount: int, future_amount: int, max_pokemons: int):
        super().__init__(
            f"you already have {current_amount} pokemons, if added you would have {future_amount}, which exceeds {max_pokemons}"
        )
