import requests
from pprint import pprint as pp

my_color = 'blue'

r = requests.get('https://pokeapi.co/api/v2/pokemon-color/blue')
resp = r.json()

pokemons = resp.get('pokemon_species')

pokemon_list = []

for pokemon in pokemons :
    this_pokemon = []
    name = pokemon.get('name')
    id = pokemon.get('url')
    id = id.split('/')
    id = id[-2]
    this_pokemon.append(name)
    this_pokemon.append(id)
    pokemon_list.append(this_pokemon)
    
for pokemon in pokemon_list:
    id = pokemon[1]
    r = requests.get('https://pokeapi.co/api/v2/pokemon-habitat/' + id)
    if r.status_code != 200 :
        pokemon.append('Unknown habitat')
        continue
    resp = r.json()
    habitat = resp.get('name')
    print(id, habitat)
    pokemon.append(habitat)
    
    ### WAAAAAAAAAAAY TOO LOOOOOOONNNNNGGGGG

pp(pokemon_list)
