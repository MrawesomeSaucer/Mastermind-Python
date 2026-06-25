# Program overview
This is a mastermind game that runs in the terminal. You can use the code as inspiration, examples or use it in your own project. Of course, you can just play it and have fun!
# How to run

## Prerequisites

- Python 3.10 or newer
- pip
- Git (optional, if cloning the repository)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MrawesomeSaucer/Mastermind-Python.git
cd Mastermind-Python
```

2. Install the project:

```bash
pip install .
```

3. Run the game:

```bash
mastermind_python
```
### Or download the ZIP

1. Download the repository as a ZIP from GitHub.
2. Extract it.
3. Open a terminal in the extracted folder.
4. Run:

```bash
pip install .
mastermind_python
```
# How to play
## Game description
Mastermind is a classic code breaking that involves logic, deduction, and strategy.
## Objective
One player, or the game itself creates a secret code, and the other player tries to guess it in as few attempts as possible. The code breaker wins by successfully guessing code based on attempts and feed backs. The code maker wins by creating a code that the code breaker cannot break.
## Gameplay
The code breaker makes a guess by inputting a sequence of color or item.
Feed back is given based on the codebeaker's guess.
- Red means the color or item is in the correct spot.
- White means the color or item is in the sequence but the wrong spot.
- Black means that the color or item is not in the sequence.

Code breaker keeps guessing until the correct sequence is guessed or number of attempts runs out.

This is a modified version of mastermind. In a real game of mastermind, feed back does not correspond to the input, but here it does. This is to allow longer sequence and longer pool and faster game play!
## Customizing
Now that you know the basics of the mastermind game. You should know about how to start a game of mastermind in this program. Before you start the game, you will have the chance to customize your game of mastermind. There are 3 modes for you to choose from: easy, hard, and custom. Think of easy and hard mode like presets, most of the customization is already set up for you. The only customization you can have in easy and hard mode are allow duplicates, mastermind and codebreaker. Allow duplicates allow you to have repeating item in your sequence which can increase the difficulty. The mastermind (code maker) can be a human or the computer will make the sequence for you, same goes for codebreaker.

Custom mode on the other hand allow you to customize all aspects of the game.
Including the two customization above in easy and hard mode, you can customize length of sequence, amount of attempts, and customize your pool (pool of item or color to make sequence and select from). The items of the pool is also no longer limited to colors. It can be number, letters and even punctuations. In total, there are 658 unique items to make pool from. So you can expand your imagination, you can have a biggest and longest mastermind game ever. Notice that if you have a sequence too long it might mess up the formatting of the playboard base on your monitor size
## Leaderboard & Scoring
If you are a codebreaker, you can enter a name to be saved on the leaderboard. After each game, a score will be given based on the difficulty of the game and your performance. The score will be save on the leaderboard under your name. And no worries, only higher scores will be saved.
You can compete with your friends to see who can have the highest score!
## Navigating
You need to navigate the program using keyboard inputs. The available options of inputs will be listed when asked for input. Just type the letter or option you want and press enter to register it. Remember that at any point of program and any input chance you can input "q" to exit the program. 
## AI
This program includes a simple and stright forward codebreaker AI. You can try it with a very large sequence as this program allows. It can be quite fun watching it solving a hundreds line sequence. You can use this AI as examples (good or bad) or as inspiration and use it in your own project.

# Author
Everything created and maintained by Haochen H

