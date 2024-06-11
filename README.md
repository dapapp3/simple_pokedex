# Generation 1 Pokedex
[![Issues](https://img.shields.io/github/issues/dapapp3/simple_pokedex.svg?style=for-the-badge)](https://github.com/dapapp3/simple_pokedex/issues)
[![GitHub forks](https://img.shields.io/github/forks/dapapp3/simple_pokedex.svg?style=for-the-badge)](https://github.com/dapapp3/simple_pokedex/network)
[![GitHub stars](https://img.shields.io/github/stars/dapapp3/simple_pokedex.svg?style=for-the-badge)](https://github.com/dapapp3/simple_pokedex/stargazers)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCbsDR27rGCFdDKQVRl_tgEQ?style=for-the-badge&logo=youtube&label=Subscribe)](https://www.youtube.com/channel/UCbsDR27rGCFdDKQVRl_tgEQ)

<img src="static/images/Banner.png" style="width: 100%;">  

This simple pokedex demonstrates how to build a web-based generation 1 pokedex using data from the PokeAPI.  

This project is a web-based Generation 1 Pokedex that brings nostalgia to Pokémon enthusiasts by showcasing vital stats and information about the original 151 Pokémon. Leveraging data initially sourced from the PokeAPI, this Pokedex allows users to explore detailed profiles of each Pokémon, including their stats, abilities, types, and more. Whether you're reminiscing about your first Pokémon adventure or discovering the classic Pokémon for the first time, this Pokedex offers a comprehensive and interactive experience.  

**Key Features:**  

- **Explore Pokémon**: Dive into detailed profiles of the original 151 Pokémon, including stats, abilities, and much more!  
- **Search Functionality**: Easily find Pokémon by name, number, or type, making it simple to locate your favorites or discover new ones.  
- **Interactive Experience**: Engage with a user-friendly interface that brings the world of Pokémon to life.  

Built with the modern web developer's toolkit, this project utilizes Python and Flask for the backend, with SQLite for data management. The frontend is crafted with HTML, CSS, and JavaScript, ensuring a responsive and interactive user experience.  

Whether you're a long-time Pokémon fan or new to the series, this Generation 1 Pokedex offers a unique way to explore the Pokémon universe. Dive in and start your journey today!

## Built With
- ![VSCode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
- ![HTML](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
- ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Usage
<img src="static/images/Home Page.PNG" alt="Pokedex Screenshot" style="width: 100%;">

Start by browsing the pokemon on the home page. Once you find one that interests you, click on its card to bring up a panel detailing just about anything you could want to know about that pokemon.

<img src="static/images/Pokemon Details Panel.png" alt="Pokemon Details Screenshot" style="width: 100%;">

In addition to the pokemon's information there is a small chance to encounter a shiny pokemon. So be sure to keep an eye out!

<img src="static/images/Shiny Pokemon.png" alt="Shiny Pokemon Screenshot" style="width: 100%;">

Finally if you're looking for a specific pokemon and don't want to scroll forever trying to find it you can use the search functionality. Pokemon are searchable by name, number, and type.

<img src="static/images/Name Search.png" alt="Search by Name" style="width: 100%;">
<img src="static/images/Number Search.png" alt="Search by Number" style="width: 100%;">
<img src="static/images/Type Search.png" alt="Search by Type" style="width: 100%;">

## Getting Started

This section provides a detailed guide on how to get the project up and running on your local machine.

### Prerequisites

- **Python**: The project requires Python 3.12. If you do not have Python installed, download and install it from [python.org](https://www.python.org/downloads/).

### Installation

Follow these steps to set up the project:

1. **Clone the Repository**

    First, you need to clone the project repository to your local machine. If you are unfamiliar with how to clone a repository, follow these steps:

    - Open your terminal (Command Prompt, PowerShell, or Terminal).
    - Navigate to the folder where you want to clone the project using the `cd` command. For example, to change to the Documents directory, you would type `cd Documents`.
    - Type the following command and press Enter:

      ```
      git clone https://github.com/your-username/your-project-name.git
      ```

    Replace `https://github.com/your-username/your-project-name.git` with the actual URL of the project repository.

2. **Install Python (if necessary)**

    If you haven't installed Python yet, download it from [python.org](https://www.python.org/downloads/) and follow the installation instructions for your operating system.

3. **Install Required Dependencies**

    After cloning the repository and ensuring Python is installed, you need to install the project's dependencies. To do this:

    - Open your terminal and navigate to the project's root directory (where you cloned the repository).
    - Run the following commands to install the necessary Python packages:

      ```
      pip install flask
      pip install requests
      ```

### Running the Project

Once you have installed all the required dependencies, you can run the project by following these steps:

1. Open your terminal and navigate to the project's root directory.
2. Run the project by typing the following command and pressing Enter:
      ```
      python app.py
      ```
3. Open your web browser and go to `http://localhost:5000` (or the URL provided in the terminal) to view the project.

Congratulations! You should now have the project running on your local machine.

## Optimizations

One of the significant optimizations made in this project was the introduction of multi-threading to handle data fetching. Initially, the code fetched data for each Pokémon, location, and move sequentially. This approach was straightforward but inefficient, as it required waiting for each request to complete before starting the next one. This led to increased overall execution time. This was especially notable as there are roughly 1,000 locations and moves in the database along with the 151 Pokemon.

To address this inefficiency, I implemented multi-threading using Python's `concurrent.futures.ThreadPoolExecutor`. This allowed me to fetch data for multiple Pokémon concurrently, significantly reducing the total time taken by these operations. Here's a brief overview of the changes made:

- **Before Optimization**: The original code executed HTTP requests in a sequential manner. For `n` Pokémon, if each request took `t` seconds, the total time would be approximately `n * t`.

- **After Optimization**: With multi-threading, multiple requests are sent out concurrently. Assuming the server can handle concurrent requests efficiently, the total time is now closer to `t` (plus some overhead for thread management), regardless of `n`.

This optimization was particularly effective for operations involving large numbers of Pokémon, where the performance improvement was several times faster than the original approach. It demonstrates the power of concurrent programming in Python for I/O-bound tasks and how a relatively simple change can lead to significant performance gains.

For illustration purposes, some sections of the code continue to use the old sequential approach (namely getting the data for the types table as there are only 21 types). Take a look at the difference in speed between collecting the type-related data and the abilities-related data.

![Performance Comparison](<static/images/Performance Comparison.gif>)

## Lessons Learned
While this was a very small and simple project, I did learn some valuable lessons. Including:

- The importance of having a well thought out roadmap for the project in advance
- How to write code defensively to handle changes from external dependencies (API)
- How to work with multi-threading in Python to speed up I/O operations

There were some features that I was unable to implement in the time I gave myself for this project due, in part, to my lack of adequate forethought on how the project would be structured when it ultimately finished. For example, adding the ability to filter the Pokémon cards list for things like base stats, abilities, or held items would be impossible without re-writing the code because the code on the home page only has access to the Pokémon's name, number, and types. Had I taken more time to think through what I wanted the user experience to be, I could've anticipated this and structured my API requests accordingly.

As I was working on this project, some of the links to the PokeAPI's website stopped working as expected. As a result, there were some moves (mainly from the newer Generation 9 games) whose pages I was unable to retrieve due to 404 status code errors. It's possible that these issues will be addressed at some point in the future, so I didn't want to simply ignore those moves. Instead, I put in try/except blocks to stop the program from crashing whenever it ran into any of these (now dead) pages, thus allowing the program to attempt retrieving move data for every move, while skipping those that are unreachable. It speaks to the importance of thinking about potential vulnerabilities in the software we write and what edge cases could conceivably arise that would cause our programs to malfunction or otherwise mislead the user.

Finally, as I covered in the Optimizations section above, I learned how to work with multi-threading libraries to significantly speed up the execution time of my program's I/O operations.

## Roadmap
- ☐ Complete Pokemon Information
  - ☐ Add Evolutions
  - ☐ Add Alternate Forms to the Pokemon details panel
- ☐ Improve Visualizations
  - ☐ Replace the table with a map that shows the Pokemon's locations
  - ☐ Replace static Pokemon sprites with animated ones 
- ☐ Add More Pokemon
  - ☐ Fetch data for Pokemon from other generations
- ☐ Team Builder
  - ☐ Allow users to add Pokemon to a team and display the team's stats, strengths, weaknesses, etc.
- ☐ Matchup Page
  - ☐ Show a Pokemon's (or team's) type coverage against other Pokemon trainers (gym leaders, elite four, etc.)
  - ☐ Show a Pokemon's (or team's) move coverage against other Pokemon trainers (gym leaders, elite four, etc.)
- ☐ Trivia Page
  - ☐ Quiz users on Pokemon stats, types, moves, and history
  - ☐ Allow users to choose the difficulty level of the quiz
  - ☐ Add leaderboards for highest accuracy and fastest time
  - ☐ Allow users to share their scores/times on social media
