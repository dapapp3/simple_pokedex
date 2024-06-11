# Import Dependencies
import requests
import sqlite3
import concurrent.futures

def main():
    # Create database tables using SQL
    with open('schema.sql', 'r') as f:
        sql = f.read()
        conn = sqlite3.connect('data/pokemon.db')
        c = conn.cursor()
        c.executescript(sql)
        conn.commit()
        conn.close()

    # Get table data
    table_data = get_table_data()
    save_table_data_to_db(table_data)

    # Get list of all Pokemon from Generation 1
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    data = response.json()
    pokemon_list = [pokemon['name'] for pokemon in data['results']]

    # Save Pokemon data retrieved from API to the database
    pokemon_data_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_single_pokemon_data, pokemon) for pokemon in pokemon_list]
        for future in concurrent.futures.as_completed(futures):
            pokemon_data = future.result()
            save_to_db(pokemon_data)
            pokemon_data_list.append(pokemon_data)
        
with requests.Session() as session:
    def get_single_pokemon_data(pokemon: str) -> dict:
        print(f"Getting data for {pokemon}")
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = session.get(url)
        data = response.json()

        # Get nested data for relevant fields (abilities, held_items, location_area_encounters, moves, stats, types)
        abilities_list = [ability['ability']['name'] for ability in data['abilities']]
        held_items_list = [item['item']['name'] for item in data['held_items']]
        locations_list = get_pokemon_location_data(data)
        moves_list = [move['move']['name'] for move in data['moves']]
        species_data = get_species_data(data)
        sprite_data = {key: data['sprites'][key] for key in ['front_default', 'back_default', 'front_shiny', 'back_shiny']}
        stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        stats_dict['base_stat_total'] = sum(stats_dict.values())
        types_list = [type['type']['name'] for type in data['types']]

        return {
            "id": data['id'],
            "name": data['name'],
            "species name": data['species']['name'],
            "height": data['height'] / 10, # API returns values in decimeters, so divide by 10 to get meters
            "weight": data['weight'] / 10, # API returns values in hectograms, so divide by 10 to get kilograms
            "abilities": abilities_list,
            "held_items": held_items_list,
            "locations": locations_list,
            "moves": moves_list,
            "species": species_data,
            "sprites": sprite_data,
            "stats": stats_dict,
            "types": types_list
        }

def get_table_data() -> dict:
    table_data = {}

    # Get Pokemon Data
    type_data = get_type_data()
    abilities_data = get_abilities_data()
    held_items_data = get_items_data()
    location_data = get_location_data()
    move_data = get_move_data()
    egg_data = get_egg_groups_data()

    table_data['types'] = type_data
    table_data['abilities'] = abilities_data
    table_data['items'] = held_items_data
    table_data['locations'] = location_data
    table_data['moves'] = move_data
    table_data['egg_groups'] = egg_data

    return table_data

def get_type_data() -> list:
    # Get all type data (if the table is empty)
    if is_table_empty('types') == False:
        return []

    all_type_data = []
    print("Getting type data")
    for i in range(1, 10):
        endpoint = f'https://pokeapi.co/api/v2/generation/{i}/'
        data = requests.get(endpoint).json()
        types = data['types']
        for type in types:
            print(f"Getting type data for {type['name']} in generation {i}")
            all_type_data.append(type['name'])
    
    return all_type_data

def get_ability_data(ability: dict, i: int) -> dict:
    print(f"Getting ability data for {ability['name']} in generation {i}")
    ability_name = ability['name']
    ability_url = ability['url']
    ability_data = requests.get(ability_url).json()

    # Set a default description in case the ability has no effect
    ability_description = None

    # Get ability effect and description (in English)
    for effect in ability_data['effect_entries']:
        if effect['language']['name'] == 'en':
            ability_description = effect['short_effect']

    return {
        "name": ability_name,
        "description": ability_description,
        "generation": i
    }

def get_abilities_data() -> list:
    if is_table_empty('abilities') == False:
        return []

    # Get all abilities data (if the table is empty)
    all_abilities_data = []

    for i in range(3, 10): # Starts at 3 because the first two generations have no abilities
        print(f"Getting abilities data for generation {i}")
        id = i
        endpoint = f'https://pokeapi.co/api/v2/generation/{id}/'
        data = requests.get(endpoint).json()
        abilities = data['abilities']

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(get_ability_data, ability, i) for ability in abilities]
            for future in concurrent.futures.as_completed(futures):
                all_abilities_data.append(future.result())

    return all_abilities_data

def get_items_data() -> list:
    if is_table_empty('items') == False:
        return []

    # Get all item data (if the table is empty)
    all_held_items_data = []
    endpoint = 'https://pokeapi.co/api/v2/item/?limit=9999'
    data = requests.get(endpoint).json()
    items = data['results']
    for item in items:
        print(f"Getting item data for {item['name']}")
        all_held_items_data.append(item['name'])
    
    return all_held_items_data

def get_egg_groups_data() -> list:
    if is_table_empty('egg_groups') == False:
        return []

    # Get all egg group data (if the table is empty)
    all_egg_groups_data = []
    endpoint = 'https://pokeapi.co/api/v2/egg-group/?limit=9999'
    data = requests.get(endpoint).json()
    egg_groups = data['results']
    for egg_group in egg_groups:
        print(f"Getting egg group data for {egg_group['name']}")
        all_egg_groups_data.append(egg_group['name'])
    
    return all_egg_groups_data

def get_single_location_data(location: dict, generations_map: dict) -> tuple:
    location_name = location['name']
    location_url = location['url']
    location_data = requests.get(location_url).json()
    location_areas = location_data['areas']
    location_id = location_data['id']
    generation = None
    print(f"Getting location data for {location['name']} ({location_data['id']})")
    for location_area in location_areas:
        location_area_url = location_area['url']
        location_area_data = requests.get(location_area_url).json()
        game_name = location_area_data['encounter_method_rates'][0]['version_details'][0]['version']['name'] if location_area_data['encounter_method_rates'] else None
        generation = generations_map[game_name] if game_name in generations_map else None
        if generation != None:
            break
    return location_name, (location_id, location_name, generation)

def get_location_data() -> dict:
    if is_table_empty('locations') == False:
        return {}
    
    # Create a generations map to match the game names to the generation number
    generations_map = {
        'red': 1,
        'green': 1,
        'blue': 1,
        'yellow': 1,
        'gold': 2,
        'silver': 2,
        'crystal': 2,
        'ruby': 3,
        'sapphire': 3,
        'emerald': 3,
        'firered': 3,
        'leafgreen': 3,
        'diamond': 4,
        'pearl': 4,
        'platinum': 4,
        'heartgold': 4,
        'soulsilver': 4,
        'black': 5,
        'white': 5,
        'black-2': 5,
        'white-2': 5,
        'x': 6,
        'y': 6,
        'omega-ruby': 6,
        'alpha-sapphire': 6,
        'sun': 7,
        'moon': 7,
        'ultra-sun': 7,
        'ultra-moon': 7,
        'letsgo-pikachu': 7,
        'letsgo-eevee': 7,
        'sword': 8,
        'shield': 8,
        'brilliant-diamond': 8,
        'shining-pearl': 8,
        'legends-arceus': 8,
        'scarlet': 9,
        'violet': 9
    }

    # Get all location data (if the table is empty)
    print("Getting location data")
    all_locations_data = {}
    endpoint = 'https://pokeapi.co/api/v2/location/?limit=9999'
    data = requests.get(endpoint).json()
    locations = data['results']

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_single_location_data, location, generations_map) for location in locations]
        for future in concurrent.futures.as_completed(futures):
            location_name, location_data = future.result()
            all_locations_data[location_name] = location_data

    return all_locations_data

def get_single_move_data(move: dict) -> dict:
    print(f"Getting move data for {move['name']}")
    move_name = move['name']
    move_url = move['url']

    # Try/except block necessary due to some API pages being inaccessible at the time of writing
    try:
        response = requests.get(move_url)
        if response.status_code == 200:
            move_data = response.json()
            return {
                "name": move_name,
                "type": move_data['type']['name'] if move_data['type'] else None,
                "power": move_data['power'],
                "accuracy": move_data['accuracy'],
                "pp": move_data['pp'],
                "priority": move_data['priority'],
                "damage_class": move_data['damage_class']['name'],
                "effect": move_data['effect_entries'][0]['short_effect'] if move_data['effect_entries'] else None,
                "effect_chance": move_data['effect_chance'],
                "ailment": move_data['meta']['ailment']['name'] if move_data['meta'] else None,
                "ailment_chance": move_data['meta']['ailment_chance'] if move_data['meta'] else None,
                "crit_rate": move_data['meta']['crit_rate'] if move_data['meta'] else None,
                "drain": move_data['meta']['drain'] if move_data['meta'] else None,
                "flinch_chance": move_data['meta']['flinch_chance'] if move_data['meta'] else None,
                "healing": move_data['meta']['healing'] if move_data['meta'] else None,
                "max_turns": move_data['meta']['max_turns'] if move_data['meta'] else None,
                "max_hits": move_data['meta']['max_hits'] if move_data['meta'] else None,
                "min_turns": move_data['meta']['min_turns'] if move_data['meta'] else None,
                "min_hits": move_data['meta']['min_hits'] if move_data['meta'] else None,
                "stat_chance": move_data['meta']['stat_chance'] if move_data['meta'] else None
            }
        else:
            print(f"Request to {move_url} for {move_name} returned status code {response.status_code}")
            return {}
    except Exception as e:
        print(f"An error occurred in get_single_move_data function: {e}")
        return {}

def get_move_data() -> list:
    if is_table_empty('moves') == False:
        return []

    # Get all moves data (if the table is empty)
    print("Getting move data")
    all_move_data = []
    endpoint = 'https://pokeapi.co/api/v2/move/?limit=9999'
    data = requests.get(endpoint).json()
    moves = data['results']

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_single_move_data, move) for move in moves]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result != {}:  # Ensures that only valid move data is added to the list
                all_move_data.append(result)

    return all_move_data

def is_table_empty(table_name: str) -> bool:
    # Connect to the SQLite database
    conn = sqlite3.connect('data/pokemon.db')
    c = conn.cursor()

    # Check if the table is empty
    c.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = c.fetchone()[0]

    # Close the connection
    conn.close()

    return count == 0

def save_table_data_to_db(table_data: dict) -> None:
    all_type_data = [(type,) for type in table_data['types']]
    all_abilities_data = [(ability['name'], ability['description'], ability['generation']) for ability in table_data['abilities']]
    all_items_data = [(item,) for item in table_data['items']]
    all_locations_data = [value for value in table_data['locations'].values()]
    all_egg_groups_data = [(egg_group,) for egg_group in table_data['egg_groups']]
    all_move_data = [(move['name'], move['type'], move['power'], move['accuracy'], move['pp'], move['damage_class']) for move in table_data['moves']]
    move_types = list(set(move[1] for move in all_move_data))
    damage_classes = list(set(move[5] for move in all_move_data))

    # Connect to the SQLite database
    conn = sqlite3.connect('data/pokemon.db')
    c = conn.cursor()

    # Insert data into the database
    c.executemany("""INSERT OR IGNORE INTO types (name) VALUES (?)""", all_type_data)
    c.executemany("""INSERT OR IGNORE INTO abilities (name, description, generation) VALUES (?, ?, ?)""", all_abilities_data)
    c.executemany("""INSERT OR IGNORE INTO items (name) VALUES (?)""", all_items_data)
    c.executemany("""INSERT OR IGNORE INTO locations (id, name, generation) VALUES (?, ?, ?)""", all_locations_data)
    c.executemany("""INSERT OR IGNORE INTO egg_groups (name) VALUES (?)""", all_egg_groups_data)
    c.executemany("""INSERT OR IGNORE INTO move_types (name) VALUES (?)""", [(move_type,) for move_type in move_types])
    c.executemany("""INSERT OR IGNORE INTO move_damage_classes (name) VALUES (?)""", [(damage_class,) for damage_class in damage_classes])

    # Get the type and damage class ids for the moves
    all_move_data_modified = []
    for move in all_move_data:
        type_id = c.execute("SELECT id FROM move_types WHERE name = ?", (move[1],)).fetchone()[0]
        damage_class_id = c.execute("SELECT id FROM move_damage_classes WHERE name = ?", (move[5],)).fetchone()[0]
        all_move_data_modified.append((move[0], type_id, move[2], move[3], move[4], damage_class_id))

    c.executemany("""INSERT OR IGNORE INTO moves (name, type_id, power, accuracy, pp, damage_class_id) VALUES (?, ?, ?, ?, ?, ?)""", all_move_data_modified)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def save_to_db(data: dict) -> None:
    # Connect to the SQLite database
    conn = sqlite3.connect('data/pokemon.db')
    c = conn.cursor()

    # Create database tables using SQL
    with open('schema.sql', 'r') as f:
        sql = f.read()
        c.executescript(sql)
    
    try:
        # Insert data into species-related tables
        pokemon_species_data = [(data['species name'], data['species']['capture_rate'], data['species']['pokedex_entry'], data['species']['growth_rate'], data['species']['is_legendary'], data['species']['is_mythical'], data['species']['pokedex_numbers'])]
        c.executemany("""INSERT OR IGNORE INTO species (name, capture_rate, pokedex_entry, growth_rate, is_legendary, is_mythical, pokedex_numbers) VALUES (?, ?, ?, ?, ?, ?, ?)""", pokemon_species_data)
        species_egg_groups_data = [(c.execute("SELECT id FROM species WHERE pokedex_numbers = ?", (data['species']['pokedex_numbers'],)).fetchone()[0], c.execute("SELECT id FROM egg_groups WHERE name = ?", (group,)).fetchone()[0]) for group in data['species']['egg_groups']]
        c.executemany("""INSERT OR IGNORE INTO species_egg_groups (species_id, egg_group_id) VALUES (?, ?)""", species_egg_groups_data)
        species_id = c.execute("SELECT id FROM species WHERE name = ?", (data['species name'],)).fetchone()[0]
        c.execute("""INSERT OR IGNORE INTO pokemon (id, name, height, weight, species_id) VALUES (?, ?, ?, ?, ?)""",
                (data['id'], data['name'], data['height'], data['weight'], species_id))
        pokemon_type_data = [(data['id'], c.execute("SELECT id FROM types WHERE name = ?", (type,)).fetchone()[0]) for type in data['types']]
        c.executemany("""INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_id) VALUES (?, ?)""", pokemon_type_data)
        pokemon_ability_data = [(data['id'], c.execute("SELECT id FROM abilities WHERE name = ?", (ability,)).fetchone()[0]) for ability in data['abilities']]
        c.executemany("""INSERT OR IGNORE INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)""", pokemon_ability_data)
        pokemon_item_data = [(data['id'], c.execute("SELECT id FROM items WHERE name = ?", (item,)).fetchone()[0]) for item in data['held_items']]
        c.executemany("""INSERT OR IGNORE INTO pokemon_held_items (pokemon_id, item_id) VALUES (?, ?)""", pokemon_item_data)
        pokemon_location_data = [(data['id'], c.execute("SELECT id FROM locations WHERE name = ?", (location,)).fetchone()[0]) for location in data['locations']]
        c.executemany("""INSERT OR IGNORE INTO pokemon_locations (pokemon_id, location_id) VALUES (?, ?)""", pokemon_location_data)
        pokemon_move_data = [(data['id'], move_row[0]) for move in data['moves'] if (move_row := c.execute("SELECT id FROM moves WHERE name = ?", (move,)).fetchone()) is not None] # Line modified due to unavailable move pages from api
        c.executemany("""INSERT OR IGNORE INTO pokemon_moves (pokemon_id, move_id) VALUES (?, ?)""", pokemon_move_data)
        c.execute("""INSERT OR IGNORE INTO sprites (id, front_default, front_shiny) VALUES (?, ?, ?)""",
                (data['id'], data['sprites']['front_default'], data['sprites']['front_shiny']))
        pokemon_sprite_data = [(data['id'], c.execute("SELECT id FROM sprites WHERE front_default = ?", (data['sprites']['front_default'],)).fetchone()[0])]
        c.executemany("""INSERT OR IGNORE INTO pokemon_sprites (pokemon_id, sprite_id) VALUES (?, ?)""", pokemon_sprite_data)
        c.execute("""INSERT OR IGNORE INTO stats (pokemon_id, hp, attack, defense, special_attack, special_defense, speed, base_stat_total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (data['id'], data['stats']['hp'], data['stats']['attack'], data['stats']['defense'], data['stats']['special-attack'], data['stats']['special-defense'], data['stats']['speed'], data['stats']['base_stat_total']))
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred in save_to_db function: {e}")
        conn.close()

    # Confirmation message
    print(f"Data has been saved to the database for {data['name']} ({data['id']})!")

def get_pokemon_location_data(pokemon: dict) -> dict:
    # Get location data
    location_url = pokemon['location_area_encounters']
    location_response = requests.get(location_url)
    location_data = location_response.json()

    # Collect encounter location data for each generation and version
    locations_list = []

    for location in location_data:
        # Go to API for location
        base_url = 'https://pokeapi.co/api/v2/location-area/'
        location_name = location['location_area']['name']
        destination_url = base_url + location_name

        # Get location data
        location_response = requests.get(destination_url)
        real_location_name = location_response.json()['location']['name'] # Needed to match the location name in the locations table (otherwise you'd get names like 'sinnoh-route-213-area' in this table and 'sinnoh-route-213' in the locations table)
        locations_list.append(real_location_name)

    return locations_list

def get_species_data(pokemon: dict) -> dict:
    # Get species data
    species_url = pokemon['species']['url']
    species_response = requests.get(species_url)
    species_data = species_response.json()

    # Get relevant info from species data
    species_dict = {
        'capture_rate': species_data['capture_rate'],
        'egg_groups': [group['name'] for group in species_data['egg_groups']],
        'pokedex_entry': [entry['flavor_text'] for entry in species_data['flavor_text_entries'] if entry['language']['name'] == 'en'][-1],
        'growth_rate': species_data['growth_rate']['name'],
        'is_legendary': species_data['is_legendary'],
        'is_mythical': species_data['is_mythical'],
        'pokedex_numbers': [entry['entry_number'] for entry in species_data['pokedex_numbers'] if entry['pokedex']['name'] == 'national'][0]
    }

    # Remove line-break characters from pokedex entry
    species_dict['pokedex_entry'] = species_dict['pokedex_entry'].replace('\n', ' ')

    return species_dict

if __name__ == "__main__":
    main()