# Import dependencies
from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon/')
def get_pokemon_card_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('data/pokemon.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("""
        SELECT 
            pokemon.id, 
            pokemon.name, 
            sprites.front_default,
            types.name as type_name
        FROM 
            pokemon
        LEFT JOIN 
            sprites ON pokemon.id = sprites.id
        LEFT JOIN
            pokemon_types ON pokemon.id = pokemon_types.pokemon_id
        LEFT JOIN
            types ON pokemon_types.type_id = types.id
    """)

    pokemon_dict = {}
    for row in cursor.fetchall():
        pokemon_id = row['id']
        name = row['name']
        sprite = row['front_default']
        type_name = row['type_name']
        if pokemon_id not in pokemon_dict:
            pokemon_dict[pokemon_id] = {
                'id': pokemon_id,
                'name': name,
                'sprite': sprite,
                'types': [],
            }
        pokemon_dict[pokemon_id]['types'].append(type_name)

    # Convert the dictionary to a list of Pokemon
    pokemon_data = list(pokemon_dict.values())

    conn.close()

    return jsonify(pokemon_data)

@app.route('/pokemon_details/<int:pokemon_id>')
def get_pokemon_details_data(pokemon_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/pokemon.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("""
        SELECT 
            pokemon.id,
            pokemon.name, 
            pokemon.height,
            pokemon.weight,
            species.*, 
            egg_groups.name AS egg_group_name,
            types.name AS type_name, 
            abilities.name AS ability_name, 
            items.name AS item_name, 
            locations.name AS location_name, 
            moves.name AS move_name, 
            move_types.name AS move_type,
            moves.power AS move_power,
            moves.accuracy AS move_accuracy,
            moves.pp AS move_pp,
            move_damage_classes.name AS damage_class,
            sprites.*, 
            stats.*
        FROM 
            pokemon
        LEFT JOIN 
            species ON pokemon.id = species.pokedex_numbers
        LEFT JOIN
            species_egg_groups ON species.id = species_egg_groups.species_id
        LEFT JOIN
            egg_groups ON species_egg_groups.egg_group_id = egg_groups.id
        LEFT JOIN 
            pokemon_types ON pokemon.id = pokemon_types.pokemon_id
        LEFT JOIN 
            types ON pokemon_types.type_id = types.id
        LEFT JOIN 
            pokemon_abilities ON pokemon.id = pokemon_abilities.pokemon_id
        LEFT JOIN 
            abilities ON pokemon_abilities.ability_id = abilities.id
        LEFT JOIN 
            pokemon_held_items ON pokemon.id = pokemon_held_items.pokemon_id
        LEFT JOIN 
            items ON pokemon_held_items.item_id = items.id
        LEFT JOIN 
            pokemon_locations ON pokemon.id = pokemon_locations.pokemon_id
        LEFT JOIN 
            locations ON pokemon_locations.location_id = locations.id
        LEFT JOIN 
            pokemon_moves ON pokemon.id = pokemon_moves.pokemon_id
        LEFT JOIN 
            moves ON pokemon_moves.move_id = moves.id
        LEFT JOIN 
            move_types ON moves.type_id = move_types.id
        LEFT JOIN 
            move_damage_classes ON moves.damage_class_id = move_damage_classes.id
        LEFT JOIN
            pokemon_sprites ON pokemon.id = pokemon_sprites.pokemon_id
        LEFT JOIN 
            sprites ON pokemon_sprites.sprite_id = sprites.id
        LEFT JOIN 
            stats ON pokemon.id = stats.pokemon_id
        WHERE 
            pokemon.id = ?
    """, (pokemon_id,))

    # Fetch all rows from the query
    rows = cursor.fetchall()

    # Initialize the dictionary to store the Pokemon data
    pokemon_data = {
        'id': None,
        'name': None,
        'height': None,
        'weight': None,
        'species': {
            'capture_rate': None,
            'egg_groups': [],
            'pokedex_entry': None,
            'growth_rate': None,
            'is_legendary': None,
            'is_mythical': None,
            'pokedex_numbers': None
        },
        'abilities': [],
        'types': [],
        'moves': [],
        'held_items': [],
        'locations': [],
        'sprites': {},
        'stats': []
    }

    # Populate the dictionary with data from the database
    for row in rows:
        if not pokemon_data['id']:
            pokemon_data['id'] = row['id']
            pokemon_data['name'] = row['name']
            pokemon_data['height'] = row['height']
            pokemon_data['weight'] = row['weight']
            pokemon_data['species']['capture_rate'] = row['capture_rate']
            pokemon_data['species']['pokedex_entry'] = row['pokedex_entry']
            pokemon_data['species']['growth_rate'] = row['growth_rate']
            pokemon_data['species']['is_legendary'] = row['is_legendary']
            pokemon_data['species']['is_mythical'] = row['is_mythical']
            pokemon_data['species']['pokedex_numbers'] = row['pokedex_numbers']
            pokemon_data['sprites'] = {
                'front_default': row['front_default'],
                'front_shiny': row['front_shiny']
            }
        
        # Add the values from each row to the lists
        if row['egg_group_name']:
            pokemon_data['species']['egg_groups'].append(row['egg_group_name']) if row['egg_group_name'] not in pokemon_data['species']['egg_groups'] else None
        if row['ability_name']:
            pokemon_data['abilities'].append(row['ability_name']) if row['ability_name'] not in pokemon_data['abilities'] else None
        if row['type_name']:
            pokemon_data['types'].append(row['type_name']) if row['type_name'] not in pokemon_data['types'] else None
        if row['move_name']:
            move_data = {
                'name': row['move_name'],
                'type': row['move_type'],
                'power': row['move_power'],
                'accuracy': row['move_accuracy'],
                'pp': row['move_pp'],
                'damage_class': row['damage_class']
            }
            if move_data not in pokemon_data['moves']:
                pokemon_data['moves'].append(move_data)
        if row['item_name']:
            pokemon_data['held_items'].append(row['item_name']) if row['item_name'] not in pokemon_data['held_items'] else None
        if row['location_name']:
            pokemon_data['locations'].append(row['location_name']) if row['location_name'] not in pokemon_data['locations'] else None
        if len(pokemon_data['stats']) == 0:
            pokemon_data['stats'].append({
                'hp': row['hp'],
                'attack': row['attack'],
                'defense': row['defense'],
                'special_attack': row['special_attack'],
                'special_defense': row['special_defense'],
                'speed': row['speed'],
                'base_stat_total': row['base_stat_total']
            })

    # Close the connection to the database
    conn.close()

    return jsonify(pokemon_data)

if __name__ == '__main__':
    app.run(debug=True)