from __future__ import annotations
from typing import List, Tuple
from hungarian_alg import Hungarian

import __init__
import random
import logging
import enum
import math
import curses
import collections


def generate_graph(game_board):
    G = {}
    white_space_coordinates = set()
    box_coordinates = set()
    target_coordinates = set()
    agent_coordinate = (0, 0)

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == "#":
                pass
            else:
                if game_board[i][j] == " ":
                    white_space_coordinates.add((i, j))
                elif game_board[i][j] == ".":
                    target_coordinates.add((i, j))

                elif game_board[i][j] == "$":
                    box_coordinates.add((i, j))

                else:
                    agent_coordinate = (i, j)

                children = []
                if j - 1 > 0 and game_board[i][j - 1] != "#":
                    children.append((i, j - 1))
                elif j + 1 < len(game_board[i]) and game_board[i][j + 1] != "#":
                    children.append((i, j + 1))
                elif i - 1 > 0 and game_board[i - 1][j] != "#":
                    children.append((i, j))

                elif i + 1 < len(game_board) and game_board[i][j + 1] != "#":
                    children.append((i, j))

                G[(i, j)] = children

    return (G, white_space_coordinates, box_coordinates, target_coordinates, agent_coordinate)


def modified_bfs(G):
    agent_coordinate = G[4]
    connected_components = []

    explored = set()

    queue = collections.deque([])

    cc = []
    while len(explored) < len(G[1]) + len(G[2]) + len(G[3]) + 1:
        if len(queue) == 0:
            connected_components.append(cc)
            cc = []
            l = G[1].union(G[3]) - explored
            l = list(l)
            queue.append(l[0])
            pass
            # add connected component and create new one
            # pick new non_target and add start bfs from there.

        else:
            node = queue.popleft()
            cc.append(node)

            if node in G[2]:
                pass
            else:
                for children in G[0][node]:
                    if children not in explored:
                        queue.append(children)

            explored.add(node)

    queue.append(agent_coordinate)

    return connected_components


def check_dead_state(game_board):
    G = generate_graph(game_board)

    connected_components = modified_bfs(G)

    if len(connected_components) > 1:
        return 0

    else:
        return 1



















logger = logging.getLogger(__name__)
_screen = None

class GameMove(enum.IntEnum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3

    def __str__(self):
        return {0: 'D', 1: 'U', 2: 'R', 3: 'L'}[self.value]


class GameState:
    """ This class holds all state related information about a game (agnostic about MCTS). """

    def __init__(self, size_h: int, size_v: int, wall_squares: List[tuple], boxes: List[tuple],
                 storage_locations: List[tuple], starting_location: tuple, move_taken_from_parent: GameMove):
        """
        :param size_h: Size of grid (h).
        :param size_v: Size of grid (v).
        :param wall_squares: List of tuples containing all walls in the game.
        :param boxes: List of tuples containing all boxes in game.
        :param storage_locations: List of tuples containing all storage locations in game.
        :param starting_location: Player starting location.
        :param move_taken_from_parent: The move taken to get to this state.
        """
        logger.debug(f'Creating new game state: {{"Boxes": {boxes}, "currentLocation": {starting_location}}}.')

        self.size_h = size_h
        self.size_v = size_v
        self.wall_squares = wall_squares.copy()
        self.boxes = boxes.copy()
        self.storage_locations = storage_locations.copy()
        self.current_location = starting_location
        self.move_taken_from_parent = move_taken_from_parent

    def return_in_2d(self):
        return [[y for y in x] for x in str(self).split('\n')][:-1]

    def __str__(self):
        """ Walls are '#', storage locations are '.', boxes are '$', and the player is '@'. """
        inside_list = lambda _v, _h, a: any(x == _h and y == _v for y, x in a)
        resultant = ''
        for _v in range(1, self.size_v + 1):
            for _h in range(1, self.size_h + 1):
                if self.current_location[1] == _h and self.current_location[0] == _v:
                    resultant = resultant + '@'
                elif inside_list(_v, _h, self.boxes):
                    resultant = resultant + '$'
                elif inside_list(_v, _h, self.storage_locations):
                    resultant = resultant + '.'
                elif inside_list(_v, _h, self.wall_squares):
                    resultant = resultant + '#'
                else:
                    resultant = resultant + ' '
            resultant = resultant + '\n'

        return resultant

    @staticmethod
    def build(filename: str) -> GameState:
        """ Create an instance of our game for some file. """
        logger.info(f'Creating game for file: {filename}.')
        f = open(filename)  # For whatever relevant file.
        params = []

        line1 = f.readline()
        params.append(int(line1[0]))  # Horizontal size.
        params.append(int(line1[2]))  # Vertical size.

        line2 = f.readline()
        real_start = line2.find(' ') + 1  # The first value in this line is the number of wall squares.
        real_line2 = line2[real_start:-1]  # (which doesnt actually matter, also taking out \n)
        num_squares = ((len(real_line2) // 2) + 1) // 2

        wall_list = []
        for i in range(num_squares):
            x = int(real_line2[4 * i])
            y = int(real_line2[(4 * i) + 2])
            wall_list.append((x, y))
        params.append(wall_list)

        line3 = f.readline()
        real_start = line3.find(' ') + 1  # The first value in this line is the number of wall squares.
        real_line3 = line3[real_start:-1]  # (which doesnt actually matter, also taking out \n)
        num_boxes = ((len(real_line3) // 2) + 1) // 2

        box_list = []
        for i in range(num_boxes):
            x = int(real_line3[4 * i])
            y = int(real_line3[(4 * i) + 2])
            box_list.append((x, y))
        params.append(box_list)

        line4 = f.readline()
        real_start = line4.find(' ') + 1  # The first value in this line is the number of wall squares.
        real_line4 = line4[real_start:-1]  # (which doesnt actually matter, also taking out \n)
        num_locs = ((len(real_line4) // 2) + 1) // 2

        loc_list = []
        for i in range(num_locs):
            x = int(real_line4[4 * i])
            y = int(real_line4[(4 * i) + 2])
            loc_list.append((x, y))
        params.append(loc_list)

        line5 = f.readline()
        start_loc = (int(line5[0]), int(line5[2]))
        params.append(start_loc)
        params.append(None)

        our_game = GameState(*params)
        GameVisualize.handle_state(our_game, 'NEW_GAME_FROM_FILE')
        return our_game

    def is_solved(self) -> bool:
        """ The game is solved if all of the boxes are in their storage locations. """
        return set(self.boxes) == set(self.storage_locations)

    def in_bad_corner(self, box_location) -> bool:
        """ Determine if we are in an unwinnable state. """
        x, y = box_location

        # Box is in a storage location. This is already solved.
        if (x, y) in self.storage_locations:
            return False

        # Box is in a corner with a wall.
        blocking_squares = set(self.wall_squares) & set(self.boxes)
        if (x - 1, y) in blocking_squares and (x, y + 1) in blocking_squares:
            return True
        if (x + 1, y) in blocking_squares and (x, y - 1) in blocking_squares:
            return True
        if (x, y + 1) in blocking_squares and (x + 1, y) in blocking_squares:
            return True
        if (x, y - 1) in blocking_squares and (x - 1, y) in blocking_squares:
            return True

        return False

    def is_terminal(self) -> bool:
        """ A game is in a terminal state if it is solved, or if it is in an unwinnable state. """
        return check_dead_state(self.return_in_2d()) == 0 or self.is_solved()
        # return self.is_solved() or any(self.in_bad_corner(x) for x in self.boxes)

    def move(self, action: GameMove) -> GameState:
        """ Move to a new state. This DOES NOT mutate our current state, rather it creates a new state. """
        new_state = GameState(self.size_h, self.size_v, self.wall_squares, self.boxes, self.storage_locations,
                              self.current_location, action)

        if action == GameMove.DOWN:
            down_loc = (new_state.current_location[0] + 1, new_state.current_location[1])
            two_away = (down_loc[0] + 1, down_loc[1])
            new_state.current_location = down_loc
            if down_loc in new_state.boxes:
                new_state.boxes.remove(down_loc)
                new_state.boxes.append(two_away)

        elif action == GameMove.UP:
            up_loc = (new_state.current_location[0] - 1, new_state.current_location[1])
            two_away = (up_loc[0] - 1, up_loc[1])
            new_state.current_location = up_loc
            if up_loc in new_state.boxes:
                new_state.boxes.remove(up_loc)
                new_state.boxes.append(two_away)

        elif action == GameMove.RIGHT:
            right_loc = (new_state.current_location[0], new_state.current_location[1] + 1)
            two_away = (right_loc[0], right_loc[1] + 1)
            new_state.current_location = right_loc
            if right_loc in new_state.boxes:
                new_state.boxes.remove(right_loc)
                new_state.boxes.append(two_away)

        elif action == GameMove.LEFT:
            left_loc = (new_state.current_location[0], new_state.current_location[1] - 1)
            two_away = (left_loc[0], left_loc[1] - 1)
            new_state.current_location = left_loc
            if left_loc in new_state.boxes:
                new_state.boxes.remove(left_loc)
                new_state.boxes.append(two_away)

        new_state._validate()  # TODO: Remove me for the final product.
        return new_state

    def get_possible_states(self) -> List[GameState]:
        """ Get all possible game states that can result from a legal action of our current game state. """
        next_states = []
        for action in self._legal_moves():
            next_states.append(self.move(action))
        return next_states

    def _legal_moves(self) -> List[GameMove]:
        """ Moves are represented here as {'down': 0, 'up': 1, 'right': 2, 'left': 3}. """
        moves = []

        down_loc = (self.current_location[0] + 1, self.current_location[1])
        if down_loc in self.boxes:
            two_away = (down_loc[0] + 1, down_loc[1])
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(GameMove.DOWN)
        if down_loc not in self.boxes and down_loc not in self.wall_squares:
            moves.append(GameMove.DOWN)

        up_loc = (self.current_location[0] - 1, self.current_location[1])
        if up_loc in self.boxes:
            two_away = (up_loc[0] - 1, up_loc[1])
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(GameMove.UP)
        if up_loc not in self.boxes and up_loc not in self.wall_squares:
            moves.append(GameMove.UP)

        right_loc = (self.current_location[0], self.current_location[1] + 1)
        if right_loc in self.boxes:
            two_away = (right_loc[0], right_loc[1] + 1)
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(GameMove.RIGHT)
        if right_loc not in self.boxes and right_loc not in self.wall_squares:
            moves.append(GameMove.RIGHT)

        left_loc = (self.current_location[0], self.current_location[1] - 1)
        if left_loc in self.boxes:
            two_away = (left_loc[0], left_loc[1] - 1)
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(GameMove.LEFT)
        if left_loc not in self.boxes and left_loc not in self.wall_squares:
            moves.append(GameMove.LEFT)

        logger.debug(f'Current legal moves: {moves}')
        return moves

    def _validate(self) -> None:
        """ For sanity checks. (Remove me for final product). """
        for box in self.boxes:
            if any(box[0] == s[0] and box[1] == s[1] for s in self.wall_squares):
                raise RuntimeError('In illegal state. Box should not be inside wall.')
            if box[0] == self.current_location[0] and box[1] == self.current_location[1]:
                raise RuntimeError('In illegal state. Box should not be inside player.')
        if any(self.current_location[0] == s[0] and self.current_location[1] == s[1] for s in self.wall_squares):
            raise RuntimeError('In illegal state. Player should not be inside wall.')


class GameModel:
    """
    - This class holds all information pertaining to evaluating a game state (keeping MCTS somewhat in mind).
    - Notes for heuristics: all heuristics MUST fit within the bound (0, 1]. They should represent some evaluation of
    a game state. If the heuristic goes beyond 1, then you must adjust the exploration_c term in MCTS.
    """

    @staticmethod
    def make_random_move(state: GameState) -> GameState:
        """ Move in some random direction. """
        return random.choice(state.get_possible_states())

    @staticmethod
    def heuristic_1(state: GameState):
        """ Heuristic 1: The ratio of the number of boxes in correct storage locations. """
        in_place = len(set(state.boxes) & set(state.storage_locations))
        resultant = 0.0000001 + in_place / float(len(state.storage_locations))
        logger.debug(f'Heuristic value 1: {resultant}')
        return resultant

    @staticmethod
    def heuristic_2(state: GameState):
        """ Heuristic 2: The number of boxes in storage locations - the number of boxes in bad states. """
        bad_boxes = 0
        for box in state.boxes:
            if state.in_bad_corner(box):
                bad_boxes = bad_boxes + 1

        in_place = len(set(state.boxes) & set(state.storage_locations))
        resultant = max(0.000001, (in_place - bad_boxes) / len(state.storage_locations))
        logger.debug(f'Heuristic value 2: {resultant}')
        return resultant

    @staticmethod
    def heuristic_3(state: GameState) -> float:
        """ Heuristic 3: Euclidean / manhattan perfect matching (Karthik can expand on this). """
        box_dict = {}
        target_dict = {}
        for i in range(1, len(state.boxes) + 1):
            box_dict[i] = state.boxes[i - 1]
            target_dict[i + 1000] = state.storage_locations[i - 1]

        bp_matrix = []
        for box in box_dict.keys():
            inner_vec = []
            for target in target_dict.keys():
                inner_vec.append(GameModel._manhattan_distance(box_dict[box], target_dict[target]))
            bp_matrix.append(inner_vec)

        logger.debug(f'Matrix: {bp_matrix}')
        hungarian = Hungarian()
        hungarian.calculate(bp_matrix)
        total_potential = hungarian.get_total_potential()

        # Factor in the minimum distance of our player to a box not in its storage location.
        min_player_distance_to_box = 10000  # Note: some arbitrary high number...
        for box in state.boxes:
            if box not in state.storage_locations:
                bad_person = GameModel._manhattan_distance(state.current_location, box)
                if min_player_distance_to_box > bad_person:
                    min_player_distance_to_box = bad_person

        resultant = min_player_distance_to_box + total_potential
        logger.debug(f'Heuristic value 3: {{ "potential": {resultant}, "player_d": {min_player_distance_to_box} }}')
        return resultant

    @staticmethod
    def heuristic_3_correction(h: float, root_h: float):
        """ Correction function to apply to incorporate heuristic 3 into the UCT formula. """
        # resultant =
        resultant = 1 - ((h / root_h) if h < root_h else 0)
        logger.debug(f'Corrected heuristic value 3: {resultant}')
        return resultant

    @staticmethod
    def _manhattan_distance(coordinate_1: Tuple, coordinate_2: Tuple) -> float:
        return abs(coordinate_1[0] - coordinate_2[0]) + abs(coordinate_1[1] - coordinate_2[1])

    @staticmethod
    def _euclidean_distance(coordinate_1: Tuple, coordinate_2: Tuple) -> float:
        return math.sqrt((coordinate_1[0] - coordinate_2[0]) ** 2 + (coordinate_1[1] - coordinate_2[1]) ** 2)


class GameVisualize:
    """ Curses manager (for the screen singleton) to help with visualizing our game. """
    @staticmethod
    def start_instance():
        global _screen
        _screen = curses.initscr()
        curses.curs_set(0)

    @staticmethod
    def kill_instance():
        curses.endwin()

    @staticmethod
    def handle_state(state: GameState, title_string: str):
        logger.debug(f'Current state:\n{state}')
        GameVisualize._update_screen(str(state), title_string)

    @staticmethod
    def _update_screen(game_string: str, title_string: str):
        global _screen
        if _screen is None:
            return

        # Start with a new screen.
        _screen.erase()

        # Pad our game string to have an equal number of characters.
        game_cols = max([len(s) for s in game_string.split('\n')])
        game_string_as_rows = [f'{s: <{game_cols}}' for s in game_string.split('\n')]
        starting_col = 0
        starting_row = 1

        # Print our title.
        _screen.addstr(starting_row - 1, starting_col, title_string)

        # Finally, print our game to the console.
        for i, row_string in enumerate(game_string_as_rows):
            _screen.addstr(starting_row + i, starting_col, row_string)
        _screen.refresh()
