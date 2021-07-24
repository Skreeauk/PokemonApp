from flask import Flask, render_template, url_for, request, redirect, flash
from functions import pokemonList, pokemonData

#pokenickname, pokename
party = [[], []]

app = Flask(__name__)
app.secret_key = b'1239fdad8sad73'

@app.route("/")
def home():
    data = pokemonList()

    party_data = []

    if len(party[1]) > 0:
        for i in range(len(party[1])):
            r_data = pokemonData(party[1][i])
            image = r_data['data']['pokemon']['sprites']['front_default']
            party_data.append([party[0][i], image])

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

    if len(party[0]) > 0:
        if pokenickname in party[0]:
            flash("Nickname already exists")
            return redirect(url_for('pokemonDetail', pokemon_name=pokename))

    party[0].append(pokenickname)
    party[1].append(pokename)
    return redirect(url_for('home'))

@app.route("/release", methods=['POST'])
def release():
    pokenickname = request.form['pokeNickname']

    for i in range(len(party[0])):
        nickname = party[0][i]
        if nickname == pokenickname:
            party[0].pop(i)
            party[1].pop(i)
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)