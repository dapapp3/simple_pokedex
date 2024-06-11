CREATE TABLE IF NOT EXISTS species (
    id INTEGER PRIMARY KEY,
    name TEXT,
    capture_rate INTEGER,
    pokedex_entry TEXT,
    growth_rate TEXT,
    is_legendary BOOLEAN,
    is_mythical BOOLEAN,
    pokedex_numbers INTEGER
);

CREATE TABLE IF NOT EXISTS egg_groups (
    id INTEGER PRIMARY KEY,
    name TEXT,
    UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS species_egg_groups (
    species_id INTEGER,
    egg_group_id INTEGER,
    PRIMARY KEY(species_id, egg_group_id),
    FOREIGN KEY(species_id) REFERENCES species(id),
    FOREIGN KEY(egg_group_id) REFERENCES egg_groups(id)
);

CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    height INTEGER, 
    weight INTEGER, 
    species_id INTEGER,
    FOREIGN KEY(species_id) REFERENCES species(id)
);

CREATE TABLE IF NOT EXISTS types (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS pokemon_types (
    pokemon_id INTEGER, 
    type_id INTEGER, 
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(type_id) REFERENCES types(id),
    PRIMARY KEY(pokemon_id, type_id),
    UNIQUE(pokemon_id, type_id)
);

CREATE TABLE IF NOT EXISTS abilities (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    description TEXT,
    generation TEXT
);

CREATE TABLE IF NOT EXISTS pokemon_abilities (
    pokemon_id INTEGER, 
    ability_id INTEGER, 
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(ability_id) REFERENCES abilities(id),
    PRIMARY KEY(pokemon_id, ability_id),
    UNIQUE(pokemon_id, ability_id)
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY, 
    name TEXT
);

CREATE TABLE IF NOT EXISTS pokemon_held_items (
    pokemon_id INTEGER, 
    item_id INTEGER, 
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(item_id) REFERENCES items(id),
    PRIMARY KEY(pokemon_id, item_id),
    UNIQUE(pokemon_id, item_id)
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    generation TEXT
);

CREATE TABLE IF NOT EXISTS pokemon_locations (
    pokemon_id INTEGER, 
    location_id INTEGER, 
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(location_id) REFERENCES locations(id),
    PRIMARY KEY(pokemon_id, location_id),
    UNIQUE(pokemon_id, location_id)
);

CREATE TABLE IF NOT EXISTS move_types (
    id INTEGER PRIMARY KEY,
    name TEXT,
    UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS move_damage_classes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS moves (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    type_id INTEGER,
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    damage_class_id INTEGER,
    FOREIGN KEY(type_id) REFERENCES move_types(id),
    FOREIGN KEY(damage_class_id) REFERENCES move_damage_classes(id)
);

CREATE TABLE IF NOT EXISTS pokemon_moves (
    pokemon_id INTEGER, 
    move_id INTEGER, 
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(move_id) REFERENCES moves(id),
    PRIMARY KEY(pokemon_id, move_id),
    UNIQUE(pokemon_id, move_id)
);

CREATE TABLE IF NOT EXISTS sprites (
    id INTEGER PRIMARY KEY,
    front_default TEXT,
    front_shiny TEXT,
    UNIQUE(front_default, front_shiny)
);

CREATE TABLE IF NOT EXISTS pokemon_sprites (
    pokemon_id INTEGER,
    sprite_id INTEGER,
    PRIMARY KEY(pokemon_id, sprite_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(sprite_id) REFERENCES sprites(id)
);

CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY, 
    pokemon_id INTEGER,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER,
    base_stat_total INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    UNIQUE(pokemon_id)
);