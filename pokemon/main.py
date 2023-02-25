# from coche import Coach
# from pokemons import Pokemon, Stats
# import asyncio

# from typing import Union

from fastapi import FastAPI

app = FastAPI()

# pokemon_names = ["bulbasaur", "pikachu", "charmander", "charmander"]
# c = Coach(name="eran", pokemons=pokemon_names)
# print(c)
# c.add_pokemons(["ditto"])
# print(c)


@app.get("/")
def read_root():
    return {"Hello": "World"}
