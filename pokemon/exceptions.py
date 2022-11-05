from constants import MAX_POKEMONS


class DuplicatePokemon(Exception):
    pass


class InvalidPokemonData(Exception):
    pass


class MaxPokemons(Exception):
    def __init__(self, current_amount: int, future_amount: int, max_pokemons: int):
        super().__init__(
            f"you already have {current_amount} pokemons, if added you would have {future_amount}, which exceeds {max_pokemons}"
        )
