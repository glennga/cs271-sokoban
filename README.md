# CS-271 Project for Team IHopeThisWorks

## Introduction
A Monte-Carlo Tree Search inspired approach to solving a Sokoban game.

## Program Structure
The bulk of our contributions are in `game_model.py` and `single_player_mcts.py`. The former contains all code related to the Sokoban game, while the latter contains all code related to MCTS. This segmentation allows us to run our AI on different games, if we so choose. All a user would need to do is specify the following: 
```python
# This must contain a *game state*, which supports the following functions:
#   1. get_possible_states()  <-- All possible states that can be reached in one action from this state.
#   2. move_taken_from_parent  <-- Field describing the move taken from the parent to reach this state.
#   3. is_terminal()  <-- Boolean that describes whether a game can progress or not.
root_node = Node(...)

mcts_instance = MCTS(
    root_node,
    simulation_bound,       # The maximum number of simulations to perform from one state.
    exploration_c,          # A number between [0, 1] that determines how much randomness should be in your search.
    uncertainty_d,          # A constant that determines how important it is that you explore some less-explored node.
    heuristic_f,            # A function with range between (0, 1]. Determines how good a leaf game state is.
    heuristic_correction_f  # If the function above does not return (0, 1], apply your correction here.
)
```

## Setup
1. Clone this repository.
```
git clone https://github.com/glennga/cs271-sokoban.git
```
2. Install Python 3.7, and setup the environment:
```
cd cs271-sokoban

# Create a new virtual environnment.
python3 -m venv venv
source venv/bin/activate

# Install our dependencies.
pip install -r requirements.txt
```
3. Run the example.
```
python3 mcts_example.py
```
If there are no dependency issues, you are good to go! 

## Visualizing the Learning Process
In an effort to help debug our processes (and also display our AI learning process in real-time), we created a command-line visualization which is invoked everytime our AI makes a move. This is enabled in the `mcts_example` code with the following commands:
```python
...
gm.Visual.start_instance()
solution = x.run(10000)
...
gm.Visual.kill_instance()
```
This requires a terminal to run (e.g. cannot be run in the Pycharm output w/o checking some boxes), but will result in an output like such:
```
SIMULATION_3
########
#  .#@.#
#$     #
#$  ## #
#   $ .#
########
```
which will update with every new game state. If you do not need to visualize this, then do not invoke `Visual.start_instance()`. By default, this visualization is not enabled.

## Insight Through Logging
In addition to the visualization mentioned previously, we also extensively log every action we perform to a log file. By default, this is located in `out/debug-output.log`. Users can change this by modifying the `logging.json` configuration file (this is a standard Python logging module dictionary config). *Be mindful of this log file size!* If the log output is too much, then reduce the log level to "INFO".

An example of log entry (this also includes an image of the game state!):
```
...
[2020-12-14 23:40:20,383][DEBUG][single_player_mcts -- _calculate_uct]: UCT of node (3, 7) from taking move None. is computed to be: 0.1875
[2020-12-14 23:40:20,383][DEBUG][single_player_mcts -- _calculate_uct]: Additional term of node (3, 7) from taking move None. is computed to be: 7.0710678118654755
[2020-12-14 23:40:20,383][DEBUG][single_player_mcts -- _calculate_uct]: Resulting UCT of node (3, 7) from taking move None. is: 7.2585678118654755
[2020-12-14 23:40:20,383][INFO][single_player_mcts -- run]: Starting iteration 1.
[2020-12-14 23:40:20,383][DEBUG][game_model -- _legal_moves]: Current legal moves: [<Action.DOWN: 0>, <Action.UP: 1>, <Action.LEFT: 3>]
[2020-12-14 23:40:20,383][DEBUG][game_model -- __init__]: Creating new game state: {"Boxes": [(3, 3), (4, 3), (4, 4)], "currentLocation": (3, 7)}.
[2020-12-14 23:40:20,383][DEBUG][game_model -- __init__]: Creating new game state: {"Boxes": [(3, 3), (4, 3), (4, 4)], "currentLocation": (3, 7)}.
[2020-12-14 23:40:20,383][DEBUG][game_model -- __init__]: Creating new game state: {"Boxes": [(3, 3), (4, 3), (4, 4)], "currentLocation": (3, 7)}.
[2020-12-14 23:40:20,384][DEBUG][game_model -- handle_state]: Current state:
########
#  .# .#
# $    #
# $$##@#
#     .#
########
```

## Experimentation (Jupyter Notebook)
All experiments regarding our various hyperparameters can be found in the notebook `tools/evaulate.ipynb`. To avoid persisting our results in the notebook, we log all experiment results to a SQLite3 database `out/results.db`. To use this notebook, a) start a Jupyter local server, b) open this notebook, and c) change the first cell `cd` command to point to your repository directory. 