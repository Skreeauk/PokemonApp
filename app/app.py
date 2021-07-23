from flask import Flask, render_template, url_for, request, redirect
import requests

url = "https://graphql-pokeapi.vercel.app/api/graphql/"

Query_Pokemon_List = """
{
pokemons(limit: 20, offset: 0)
    {
        count
        next
        previous
        nextOffset
        prevOffset
        status
        message
        results 
        {
            url
            name
            image
        }
    }
}
"""

Query_Pokemon_Data = """
{
    pokemon(name: "bulbasaur") {
        id
        name
        sprites {
            front_default
        }
        moves {
            move {
                name
            }
        }
        types {
            type {
                name
            }
        }
    }
}
"""

party = []

app = Flask(__name__)

@app.route("/")
def home():
    r = requests.post(url, json={'query': Query_Pokemon_List})
    r_data = r.json()
    data = r_data['data']['pokemons']['results']

    party_data = []

    if len(party) > 0:
        for pokemon in party:

            query1 = 'pokemon(name: "{}")'.format(pokemon[1])
            query2 = '''
                {
                    id
                    name
                    sprites {
                        front_default
                    }
                    moves {
                        move {
                            name
                        }
                    }
                    types {
                        type {
                            name
                        }
                    }
                }
            }'''
            query = '{' + query1 + query2
            r = requests.post(url, json={'query': query})
            r_data = r.json()
            image = r_data['data']['pokemon']['sprites']['front_default']
            party_data.append((pokemon[0], image))

    return render_template('home.html', data=data, party=party_data)

@app.route("/<string:pokemon_name>")
def pokemon(pokemon_name):
    query1 = 'pokemon(name: "{}")'.format(pokemon_name)
    query2 = '''
    {
        id
        name
        sprites {
            front_default
        }
        moves {
            move {
                name
            }
        }
        types {
            type {
                name
            }
        }
    }
}'''
    query = '{' + query1 + query2
    r = requests.post(url, json={'query': query})
    r_data = r.json()
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

if __name__ == '__main__':
    app.run(debug=True)