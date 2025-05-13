![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

Flip and Find is a fun and interactive memory card-matching game.  Players test their memory by flipping cards to find matching symbol pairs. The game includes three difficulty levels, a timer, move counter, and a celebratory popup when all pairs are matched! **May 14, 2024**

## User Experience

### First-Time Visitor Goals

- Quickly start a game with clear instructions.
- Simple, engaging interface and responsive design.

### Returning Visitor Goals

- Choose a higher difficulty for more challenge.
- Compete for better times and fewer moves.

## Features

- Difficulty Selection: Easy, Medium, and Hard levels with increasing grid sizes.
- Card Flipping Logic: Cards flip to reveal emojis/images; unmatched pairs flip back.
- Move Counter & Timer: Tracks the number of moves and time taken for each game.
- Congratulation Popup: Semi-transparent overlay appears when all pairs are found.

## Future Features

- A scoring system based on speed and accuracy.
- Player name entry and leaderboard.

## Design

- The GUI is built with Tkinter and designed to be intuitive:
- Sidebar showing a main menu with the difficulty levels, timer, moves and Start Game/New Game button.
- Cards laid out in a grid according to difficulty.
- Consistent styling across screens for a smooth user experience.
hi- A congratulation overlay provides closure after game completion.

## Development Process

1. Card Logic & Matching: Implementing the game’s memory logic using Python classes and random.shuffle.
2. GUI Design: Designing with Tkinter widgets and frames.
3. Timer & Move Tracking: Using after() method to update time and moves.
4. Overlay Implementation: Semi-transparent canvas layer for endgame popup.


- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
