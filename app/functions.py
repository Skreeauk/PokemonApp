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

def pokemonList():
    r = requests.post(url, json={'query': Query_Pokemon_List})
    r_data = r.json()
    data = r_data['data']['pokemons']['results']
    return data

def pokemonData(name):
    query1 = 'pokemon(name: "{}")'.format(name)
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
    return r_data