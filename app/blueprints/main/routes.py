from flask import render_template, request
import requests
from flask_login import login_required
from .import bp as main


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/trainers', methods=['GET'])
@login_required
def trainers():
    my_trainers = ["Ash", "Misty", "Brock", "Garry"]
    # name inside of HTML = name in python
    return render_template("trainers.html.j2", trainers=my_trainers)


@main.route('/pokedex', methods=['GET', 'POST'])
@login_required
def pokedex():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        # sprites = request.form.get('sprites')
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url)

        if response.ok:
            # request worked
            if not response.json():
                error_string = "We have a problem loading the database"
                return render_template('pokedex.html.j2', error=error_string)
            data = response.json()
            pokemon_dict = {}
            pokemon = {
                "Name": data['forms'][0]['name'],
                "Base Stat HP": data['stats'][0]['base_stat'],
                "Base Stat Defense": data['stats'][1]['base_stat'],
                "Base Stat Attack": data['stats'][2]['base_stat'],
                "Sprite URL": data['sprites']['front_shiny']
            }
            print(pokemon)
            return render_template('pokedex.html.j2', pokemon=pokemon)

        else:
            error_string = "The database is on lunch break"
            return render_template('pokedex.html.j2', error=error_string)
    # the request fail

    return render_template('pokedex.html.j2')
