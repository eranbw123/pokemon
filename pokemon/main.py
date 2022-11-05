from coche import Coach
from pokemons import Pokemon, Stats
import asyncio


# pokemon_names = ["bulbasaur", "pikachu", "charmander", "charmander"]
# c = Coach(name="eran", pokemons=pokemon_names)
# print(c)
# c.add_pokemons(["ditto"])
# print(c)

pic = Pokemon("test", 1, ["1", "2"], Stats(1, 2, 3, 4, 5, 6))
pokemons = asyncio.run(pic.fetch_pokemons(["test"]))

print(pokemons)
