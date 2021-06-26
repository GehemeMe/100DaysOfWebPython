from program import app
from flask import render_template, request
from datetime import datetime
import requests


@app.route('/')
@app.route('/index')
def index():
    timenow = str(datetime.today())
    return render_template('index.html', time=timenow)

@app.route('/100Days')
def p100Days():
    return render_template('100Days.html')



@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)

def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']



@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    error = []
    if request.method == 'POST' and 'pokecolor' in request.form:
        color = request.form.get('pokecolor')
        if possible_colors(color):
            pokemon = get_poke_colors(color)
        else:
            error.append('Color invalid, please correct it.')
    return render_template('pokemon.html', pokemon=pokemon, error=error)


def get_poke_colors(color):
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + color.lower())
    pokedata = r.json()
    pokemon = []
    
    for i in pokedata['pokemon_species']:
        pokemon.append(i['name'])
        
    return pokemon

def possible_colors(color):
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color')
    resp = r.json()
    colors = [i.get('name') for i in resp['results']]
    return color in colors

