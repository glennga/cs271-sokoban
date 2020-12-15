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


logger = logging.getLogger(__name__)
_screen = None

class Action(enum.IntEnum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3

    def __str__(self):
        return {0: 'D', 1: 'U', 2: 'R', 3: 'L'}[self.value]


class State:
    """ This class holds all state related information about a game (agnostic about MCTS). """

    def __init__(self, size_h: int, size_v: int, wall_squares: List[tuple], boxes: List[tuple],
                 storage_locations: List[tuple], starting_location: tuple, move_taken_from_parent: Action):
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
    def build(filename: str) -> State:
        """ Create an instance of our game for some file. """
        create_list_from_string = lambda a: [(int(a[i]), int(a[i + 1])) for i in range(0, int(len(a)), 2)]
        logger.info(f'Creating game for file: {filename}.')
        f = open(filename)  # For whatever relevant file.

        line1 = f.readline().strip().split(' ')
        h_size, v_size = int(line1[0]), int(line1[1])

        line2 = f.readline()
        real_start = line2.find(' ') + 1
        wall_list = create_list_from_string(line2[real_start:-1].strip().split(' '))

        line3 = f.readline()
        real_start = line3.find(' ') + 1
        box_list = create_list_from_string(line3[real_start:-1].strip().split(' '))

        line4 = f.readline()
        real_start = line4.find(' ') + 1
        loc_list = create_list_from_string(line4[real_start:-1].strip().split(' '))

        line5 = f.readline().strip().split(' ')
        start_loc = (int(line5[0]), int(line5[1]))

        our_game = State(**{
            'size_h': h_size,
            'size_v': v_size,
            'wall_squares': wall_list,
            'boxes': box_list,
            'storage_locations': loc_list,
            'starting_location': start_loc,
            'move_taken_from_parent': None
        })
        Visual.handle_state(our_game, 'NEW_GAME_FROM_FILE')
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
        blocking_squares = set(self.wall_squares)
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
        # return check_dead_state(self.return_in_2d()) == 0 or self.is_solved()
        return self.is_solved() or any(self.in_bad_corner(x) for x in self.boxes)

    def move(self, action: Action) -> State:
        """ Move to a new state. This DOES NOT mutate our current state, rather it creates a new state. """
        new_state = State(self.size_h, self.size_v, self.wall_squares, self.boxes, self.storage_locations,
                          self.current_location, action)

        if action == Action.DOWN:
            down_loc = (new_state.current_location[0] + 1, new_state.current_location[1])
            two_away = (down_loc[0] + 1, down_loc[1])
            new_state.current_location = down_loc
            if down_loc in new_state.boxes:
                new_state.boxes.remove(down_loc)
                new_state.boxes.append(two_away)

        elif action == Action.UP:
            up_loc = (new_state.current_location[0] - 1, new_state.current_location[1])
            two_away = (up_loc[0] - 1, up_loc[1])
            new_state.current_location = up_loc
            if up_loc in new_state.boxes:
                new_state.boxes.remove(up_loc)
                new_state.boxes.append(two_away)

        elif action == Action.RIGHT:
            right_loc = (new_state.current_location[0], new_state.current_location[1] + 1)
            two_away = (right_loc[0], right_loc[1] + 1)
            new_state.current_location = right_loc
            if right_loc in new_state.boxes:
                new_state.boxes.remove(right_loc)
                new_state.boxes.append(two_away)

        elif action == Action.LEFT:
            left_loc = (new_state.current_location[0], new_state.current_location[1] - 1)
            two_away = (left_loc[0], left_loc[1] - 1)
            new_state.current_location = left_loc
            if left_loc in new_state.boxes:
                new_state.boxes.remove(left_loc)
                new_state.boxes.append(two_away)

        new_state._validate()  # TODO: Remove me for the final product.
        return new_state

    def get_possible_states(self) -> List[State]:
        """ Get all possible game states that can result from a legal action of our current game state. """
        next_states = []
        for action in self._legal_moves():
            next_states.append(self.move(action))
        return next_states

    def _legal_moves(self) -> List[Action]:
        """ Moves are represented here as {'down': 0, 'up': 1, 'right': 2, 'left': 3}. """
        moves = []

        down_loc = (self.current_location[0] + 1, self.current_location[1])
        if down_loc in self.boxes:
            two_away = (down_loc[0] + 1, down_loc[1])
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(Action.DOWN)
        if down_loc not in self.boxes and down_loc not in self.wall_squares:
            moves.append(Action.DOWN)

        up_loc = (self.current_location[0] - 1, self.current_location[1])
        if up_loc in self.boxes:
            two_away = (up_loc[0] - 1, up_loc[1])
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(Action.UP)
        if up_loc not in self.boxes and up_loc not in self.wall_squares:
            moves.append(Action.UP)

        right_loc = (self.current_location[0], self.current_location[1] + 1)
        if right_loc in self.boxes:
            two_away = (right_loc[0], right_loc[1] + 1)
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(Action.RIGHT)
        if right_loc not in self.boxes and right_loc not in self.wall_squares:
            moves.append(Action.RIGHT)

        left_loc = (self.current_location[0], self.current_location[1] - 1)
        if left_loc in self.boxes:
            two_away = (left_loc[0], left_loc[1] - 1)
            if two_away not in self.boxes and two_away not in self.wall_squares:
                moves.append(Action.LEFT)
        if left_loc not in self.boxes and left_loc not in self.wall_squares:
            moves.append(Action.LEFT)

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


class Evaluation:
    """
    - This class holds all information pertaining to evaluating a game state (keeping MCTS somewhat in mind).
    - Notes for heuristics: all heuristics MUST fit within the bound (0, 1]. They should represent some evaluation of
    a game state. If the heuristic goes beyond 1, then you must adjust the exploration_c term in MCTS.
    """

    @staticmethod
    def make_random_move(state: State) -> State:
        """ Move in some random direction. """
        return random.choice(state.get_possible_states())

    @staticmethod
    def heuristic_1(state: State):
        """ Heuristic 1: The ratio of the number of boxes in correct storage locations. """
        in_place = len(set(state.boxes) & set(state.storage_locations))
        resultant = 0.0000001 + in_place / float(len(state.storage_locations))
        logger.debug(f'Heuristic value 1: {resultant}')
        return resultant

    @staticmethod
    def heuristic_2(state: State):
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
    def heuristic_3(state: State) -> float:
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
                inner_vec.append(Evaluation._manhattan_distance(box_dict[box], target_dict[target]))
            bp_matrix.append(inner_vec)

        logger.debug(f'Matrix: {bp_matrix}')
        hungarian = Hungarian()
        hungarian.calculate(bp_matrix)
        total_potential = hungarian.get_total_potential()

        # Factor in the minimum distance of our player to a box not in its storage location.
        min_player_distance_to_box = 10000  # Note: some arbitrary high number...
        for box in state.boxes:
            if box not in state.storage_locations:
                bad_person = Evaluation._manhattan_distance(state.current_location, box)
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


class Visual:
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
    def handle_state(state: State, title_string: str):
        logger.debug(f'Current state:\n{state}')
        Visual._update_screen(str(state), title_string)

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
