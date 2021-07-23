from flask import Flask, render_template, url_for, request, redirect
import requests
from functions import pokemonList, pokemonData

url = "https://graphql-pokeapi.vercel.app/api/graphql/"

party = []

app = Flask(__name__)

@app.route("/")
def home():
    data = pokemonList()

    party_data = []

    if len(party) > 0:
        for pokemon in party:

            r_data = pokemonData(pokemon[1])
            image = r_data['data']['pokemon']['sprites']['front_default']
            party_data.append((pokemon[0], image))

    return render_template('home.html', data=data, party=party_data)

@app.route("/<string:pokemon_name>")
def pokemonDetail(pokemon_name):
    r_data = pokemonData(pokemon_name)
    image = r_data['data']['pokemon']['sprites']['front_default']
    moves = r_data['data']['pokemon']['moves']
    types = r_data['data']['pokemon']['types']
    return render_template('pokemon.html', name=pokemon_name, image=image, moves=moves, types=types)

@app.route("/rename", methods=['POST'])
def rename():
    pokenickname = request.form['pokeNickname']
    pokename = request.form['pokeName']
    party.append((pokenickname, pokename))
    return redirect(url_for('home'))

@app.route("/release")
def release():
    party.pop()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)