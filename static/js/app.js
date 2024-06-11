// Chart IDs
let chartIDs = {};

// Type Colors
const typeColors = {
    normal: '#A8A77A',
    fighting: '#C22E28',
    flying: '#A98FF3',
    poison: '#A33EA1',
    ground: '#E2BF65',
    rock: '#B6A136',
    bug: '#A6B91A',
    ghost: '#735797',
    fire: '#EE8130',
    water: '#6390F0',
    grass: '#7AC74C',
    electric: '#F7D02C',
    psychic: '#F95587',
    ice: '#96D9D6',
    dragon: '#6F35FC',
    steel: '#B7B7CE',
    dark: '#705746',
    unknown: 'linear-gradient(to bottom, #b0d8d4 50%, #e9658f 50%)',
    shadow: '#CB9AEF',
    fairy: '#D685AD'
};

// Initialize the application
function _init() {
    // Add an event listener to the search bar
    const searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('input', handleSearchInput);

    // Get the cards from the Flask API
    getCards();
}

// Destroy the charts (if they exist)
function destroyCharts() {
    for (let chartID in chartIDs) {
        if (chartIDs[chartID]) {
            chartIDs[chartID].destroy();
        }
    }
}

// Convert hex to rgba
function hexToRgba(hex, opacity) {
    const r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);

    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + opacity + ')';
}

// Convert a string to Title Case
function capitalizeWords(str) {
    // Capitalize the word 'hp' as 'HP'
    if (str === 'hp') {
        return str.toUpperCase();
    }

    // Replace underscores with spaces before splitting
    str = str.replace(/_/g, ' ');

    // Split the string into words and convert to Title Case
    return str.split(' ').map(function(word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }).join(' ');
}

// Filter visible cards based on search bar input
function handleSearchInput() {
    // Get the current value of the search bar and convert it to lowercase
    const searchValue = this.value.toLowerCase();

    // Get all the column divs
    const cols = document.querySelectorAll('#pokemon-cards > div');

    // Loop through all the column divs
    cols.forEach(col => {
        // Get the card's title & types and convert them to lowercase
        const cardTitle = col.querySelector('.card-title').textContent.toLowerCase();
        const cardTypes = Array.from(col.querySelectorAll('.card-text .type')).map(type => type.textContent.toLowerCase());

        // Check if the card's title or any of its types include the search bar's value
        if (cardTitle.includes(searchValue) || cardTypes.some(type => type.includes(searchValue))) {
            // If it does, show the column div
            col.style.display = '';
        } else {
            // Otherwise, hide the column div
            col.style.display = 'none';
        }
    });
}

// Get the data from the Flask route
function getCards() {
    fetch('/pokemon/').then(response => response.json()).then(data => {
        loadCards(data);
    });
}

// Load the cards into the html
function loadCards(cards) {
    // Get the card's parent element
    const cardsContainer = document.getElementById('pokemon-cards');

    // Loop through the array and create a card for each Pokemon
    for (let i = 0; i < cards.length; i++) {
        const cardColumn = document.createElement('div');
        cardColumn.className = 'col-lg-2 col-md-4 col-sm-6';

        const card = document.createElement('div');
        card.className = 'card';

        // Add an event listener to the card that opens the pokemon details when the card is clicked
        (function(i) {
            card.addEventListener('click', function() {
                getPokemonDetails(cards[i].id);
            });
        })(i);

        // Create the card
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        const cardTitle = document.createElement('h5');
        cardTitle.className = 'card-title';
        const capitalizedPokemonName = capitalizeWords(cards[i].name);
        cardTitle.textContent = capitalizedPokemonName + ' (#' + cards[i].id + ')';

        const cardImage = document.createElement('img');
        cardImage.className = 'card-img-top';
        cardImage.src = cards[i].sprite;

        const cardTypes = document.createElement('div');
        cardTypes.className = 'card-text';

        for (let j = 0; j < cards[i].types.length; j++) {
            const typeSpan = document.createElement('span');
            typeSpan.className = 'type ' + cards[i].types[j];
            typeSpan.textContent = cards[i].types[j];

            cardTypes.appendChild(typeSpan);
        }

        // Append the title, image, and types to the card body
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardImage);
        cardBody.appendChild(cardTypes);

        // Append the card body to the card
        card.appendChild(cardBody);

        // Append the card to the card column
        cardColumn.appendChild(card);

        // Append the card column to the container
        cardsContainer.appendChild(cardColumn);
    }
}

// Get the Pokemon's details from the Flask API
function getPokemonDetails(pokemon_id) {
    fetch(`/pokemon_details/${pokemon_id}`)
        .then(response => response.json())
        .then(pokemon => {
            displayPokemonDetails(pokemon);
        });
}

// Display the Pokemon's details in a panel
function displayPokemonDetails(pokemon) {
    // Get the panel and its elements
    const pokemonDetails = document.getElementById('pokemonDetailsPanel');
    const pokemonDetailsTitle = document.getElementById('pokemonDetailsPanelTitle');
    const pokemonDetailsImage = document.getElementById('pokemonDetailsPanelImage');
    const pokemonDetailsTypes = document.getElementById('pokemonDetailsPanelTypes');
    const pokedexEntry = document.getElementById('pokemonDetailsPanelPokedexEntry');

    // Show the panel
    pokemonDetails.style.display = 'flex';
    document.getElementById('overlay').style.display = 'block';

    // Set display values
    displayPokemonStatus(pokemon, pokemonDetailsTitle);
    displayPokemonProfile(pokemon, pokemonDetailsTitle);
    displayPokemonTypes(pokemon, pokemonDetails, pokemonDetailsTypes);
    displayPokemonStats(pokemon);
    displayPokemonMoves(pokemon);
    displayPokemonLocations(pokemon);
    pokemonDetailsImage.src = Math.floor(Math.random() * 5) + 1 === 1 ? pokemon.sprites.front_shiny : pokemon.sprites.front_default;
    pokedexEntry.textContent = pokemon.species.pokedex_entry;

    // Add an event listener to the close button
    document.getElementById('closepokemonDetailsPanel').addEventListener('click', function() {
        pokemonDetails.style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
        destroyCharts();
    });
}

// Color the Pokemon's name based on its legendary/mythical status
function displayPokemonStatus(pokemon, pokemonDetailsTitle) {
    if (pokemon.species.is_legendary) {
        pokemonDetailsTitle.style.color = 'yellow';
    } else if (pokemon.species.is_mythical) {
        pokemonDetailsTitle.style.color = 'skyblue';
    } else {
        pokemonDetailsTitle.style.color = 'white';
    }
}

// Display the Pokemon's profile information (height, weight, abilities, etc.)
function displayPokemonProfile(pokemon, pokemonDetailsTitle) {
    const capitalizedPokemonName = capitalizeWords(pokemon.name);
    pokemonDetailsTitle.textContent = capitalizedPokemonName + ' (#' + pokemon.id + ')';

    // Get the value spans within the grid items
    const heightValue = document.querySelector('.profile-item-height .profile-item-value');
    const weightValue = document.querySelector('.profile-item-weight .profile-item-value');
    const abilitiesValue = document.querySelector('.profile-item-abilities .profile-item-value');
    const eggGroupsValue = document.querySelector('.profile-item-egg-groups .profile-item-value');
    const captureRateValue = document.querySelector('.profile-item-capture-rate .profile-item-value');
    const growthRateValue = document.querySelector('.profile-item-growth-rate .profile-item-value');
    const heldItemsValue = document.querySelector('.profile-item-held-items .profile-item-value');

    // Set the textContent or innerHTML of each value span
    heightValue.textContent = pokemon.height + ' m';
    weightValue.textContent = pokemon.weight + ' kg';
    abilitiesValue.textContent = pokemon.abilities.join(', ');
    eggGroupsValue.textContent = pokemon.species.egg_groups.join(', ');
    captureRateValue.textContent = pokemon.species.capture_rate;
    growthRateValue.textContent = pokemon.species.growth_rate;
    if (pokemon.held_items.length === 0) {
        heldItemsValue.textContent = 'None';
    } else {
        heldItemsValue.textContent = pokemon.held_items.join(', ');
    }

    // Resize the profile wrapper y-axis to fit the content
    const profileWrapper = document.querySelector('.profile-wrapper');
    profileWrapper.style.height = 'auto';

}

// Display the Pokemon's types in the panel
function displayPokemonTypes(pokemon, pokemonDetails, pokemonDetailsTypes) {
    // Clear the panel types (otherwise types from previous Pokemon will still be there)
    pokemonDetailsTypes.innerHTML = '';

    // Create a span for each type and append it to the panel types
    for (let i = 0; i < pokemon.types.length; i++) {
        const typeSpan = document.createElement('span');
        typeSpan.className = 'type ' + pokemon.types[i];
        typeSpan.textContent = pokemon.types[i];
        pokemonDetailsTypes.appendChild(typeSpan);
    }

    // Set the background color of the panel using the color associated with first type of the Pokemon
    const typeColor = typeColors[pokemon.types[0]];
    const rgbaColor = hexToRgba(typeColor, 0.7);
    pokemonDetails.style.backgroundColor = rgbaColor;
}

// Display the Pokemon's stats in a horizontal bar chart using Chart.js
function displayPokemonStats(pokemon) {
    const statOrder = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'];
    const allStats = pokemon.stats[0];
    const statNames = statOrder;
    const formattedStatNames = statNames.map(capitalizeWords);
    const statValues = statOrder.map(stat => allStats[stat]);
    const statColorMap = {
        hp: '#69DC12',
        attack: '#EFCC18',
        defense: '#E86412',
        special_attack: '#14C3F1',
        special_defense: '#4A6ADF',
        speed: '#D51DAD'
    };

    // Create the chart
    const ctx = document.getElementById('pokemonStatsChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: formattedStatNames,
            datasets: [{
                label: 'Base Stat',
                data: statValues,
                backgroundColor: statNames.map(stat => statColorMap[stat] || 'rgba(0, 123, 255, 0.5)'),
                borderColor: statNames.map(stat => statColorMap[stat] || 'rgba(0, 123, 255, 1)'),
                borderWidth: 1,
                barPercentage: 0.95,
                categoryPercentage: 1.0,
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    min: 0,
                    max: 255,
                    ticks: {
                        display: false,
                    },
                    grid: {
                        display: false,
                    }
                }
            },
            elements: {
                bar: {
                    borderWidth: 2
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
                title: {
                    display: false,
                },
                tooltip: {
                    enabled: false,
                },
                datalabels: {
                    color: 'white',
                    display: true,
                    align: 'center',
                    anchor: 'center',
                    formatter: function(value, context) {
                        return value;
                    },
                    textShadowColor: 'black',
                    textShadowBlur: 4,
                    font: {
                        weight: 'bold',
                        size: 20,
                    },
                }
            }
        }
    });

    // Add chart object to chartIDs to allow for future chart destruction
    chartIDs['pokemonStatsChart'] = myChart;

    return myChart;
}

// Display the Pokemon's learnset in a table
function displayPokemonMoves(pokemon) {
    // Get the learnset table body
    const learnsetTableBody = document.querySelector('#learnsetTableBody');

    // Clear any existing rows from the table
    while (learnsetTableBody.firstChild) {
        learnsetTableBody.removeChild(learnsetTableBody.firstChild);
    }

    // Add a new row for each move
    pokemon.moves.forEach((move, index) => {
        const row = document.createElement('tr');
        const moveNumberCell = document.createElement('td');
        const moveNameCell = document.createElement('td');
        const moveTypeCell = document.createElement('td');
        const movePowerCell = document.createElement('td');
        const moveAccuracyCell = document.createElement('td');
        const movePPCell = document.createElement('td');
        const moveDamageClassCell = document.createElement('td');

        moveNumberCell.textContent = index + 1;
        moveNameCell.textContent = capitalizeWords(move.name.replace(/-/g, ' '));
        moveTypeCell.textContent = capitalizeWords(move.type);
        movePowerCell.textContent = move.power !== null ? move.power : 'N/A';
        moveAccuracyCell.textContent = move.accuracy !== null ? move.accuracy : 'N/A';
        movePPCell.textContent = move.pp;
        moveDamageClassCell.textContent = capitalizeWords(move.damage_class);

        row.appendChild(moveNumberCell);
        row.appendChild(moveNameCell);
        row.appendChild(moveTypeCell);
        row.appendChild(movePowerCell);
        row.appendChild(moveAccuracyCell);
        row.appendChild(movePPCell);
        row.appendChild(moveDamageClassCell);
        learnsetTableBody.appendChild(row);
    });
}

// Display the Pokemon's locations in a table (if any)
function displayPokemonLocations(pokemon) {
    // Get the location table & body
    const locationTable = document.getElementById('pokemonDetailsPanelLocations');
    const locationTableBody = document.querySelector('#locationTableBody');

    // Get the grid container
    const gridContainer = document.querySelector('.grid-container');

    // Clear any existing rows from the table
    while (locationTableBody.firstChild) {
        locationTableBody.removeChild(locationTableBody.firstChild);
    }

    // Check if the pokemon has any locations
    if (pokemon.locations.length === 0) {
        // If not, hide the table and adjust the grid container
        locationTable.style.display = 'none';
        gridContainer.style.gridTemplateAreas = `
            "title title"
            "image profile"
            "types pokedex-entry"
            "stats stats"
            "learnset learnset"
            "button button"
        `;
    } else {
        // Otherwise, show the table, add a new row for each location, and adjust the grid container
        locationTable.style.display = 'block';
        gridContainer.style.gridTemplateAreas = `
            "title title"
            "image profile"
            "types pokedex-entry"
            "stats stats"
            "learnset location"
            "button button"
        `;

        pokemon.locations.forEach((location, index) => {
            const row = document.createElement('tr');
            const locationNumberCell = document.createElement('td');
            const locationNameCell = document.createElement('td');

            locationNumberCell.textContent = index + 1;
            locationNameCell.textContent = capitalizeWords(location.replace(/-/g, ' '));

            row.appendChild(locationNumberCell);
            row.appendChild(locationNameCell);
            locationTableBody.appendChild(row);
        });
    }
}

// Register the Chart.js datalabels plugin
Chart.register(ChartDataLabels);

// Call init function on page load
document.addEventListener('DOMContentLoaded', _init);