from __future__ import annotations
from typing import List, Union
from typing import Callable
from collections import deque

import __init__
import game_model as gm
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Node:
    """ A node in our search space. """
    def __init__(self, state: gm.State):
        self.state = state
        self.h_sum = 0
        self.h_sum_sq = 0
        self.visits = 0
        self.parent = None
        self.children = []
        self.sp_uct = 0.0

    def add_child(self, child: Node):
        self.children.append(child)
        child.parent = self

    def is_descendant(self) -> bool:
        return self.parent is not None

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def __str__(self):
        return f'{str(self.state.current_location)} from taking move {str(self.state.move_taken_from_parent)}.'


class Solution:
    """ A sequence of moves that take the root state to a solved state. """
    def __init__(self, node: Node, simulated_moves: deque, number_of_iterations: int):
        self.number_of_iterations = number_of_iterations
        self.move_sequence = simulated_moves

        # Append the moves of our parents, all the way to the root.
        current_node = node
        while current_node.is_descendant():
            self.move_sequence.appendleft(current_node.state.move_taken_from_parent)
            current_node = current_node.parent

    def __iter__(self):
        self.working_index = 0
        return self

    def __next__(self):
        if self.working_index < len(self.move_sequence):
            resultant = self.move_sequence[self.working_index]
            self.working_index += 1
            return resultant

        else:
            raise StopIteration

    def __str__(self):
        output_str = ''

        previous_move, current_move_count = None, 1
        for move in self.move_sequence:
            if previous_move != move:
                output_str += f'{current_move_count} {str(move)} '
                current_move_count = 1
            else:
                current_move_count += 1
            previous_move = move

        # Account for the tail.
        if current_move_count > 1:
            output_str += f'{current_move_count} {str(previous_move)} '

        return output_str


class MCTS:
    def __init__(self, root: Node, heuristic_f: Callable, simulation_bound: int = 20, exploration_c: float = 0.5,
                 uncertainty_d: float = 50, heuristic_correction_f: Callable = lambda h, root_h: h):
        self.root = root
        self.simulation_bound = simulation_bound
        self.exploration_c = exploration_c
        self.uncertainty_d = uncertainty_d

        self.heuristic_f = heuristic_f
        self.heuristic_correction_f = heuristic_correction_f

    def run(self, iterations: int) -> Union[Solution, None]:
        """
        1. For the given amount of iterations...
        2. Select a leaf node and expand it.
        3. If we have not reached a terminal state, then simulate and backpropagate.
        4. If-- while simulating we have found a solution, exit early.
        5. Otherwise, backpropagate our result.
        :return None if no solution. Otherwise, the solution to the given problem.
        """
        for i in range(iterations):
            logger.info(f'Starting iteration {i}.')
            x = self._selection()
            y = self._expansion(x)

            if y is not None:
                h = self._simulation(y, i)
                if isinstance(h, Solution):
                    logger.info(f'Solution has been found in {i + 1} iterations!')
                    logger.info(f'Solution is: {str(h)}')
                    return h

                self._back_propagation(y, h)
            else:
                h = self.heuristic_f(x.state)
                self._back_propagation(x, h)

        logger.info('Search has timed out, no solution found.')
        return None

    @staticmethod
    def _pick_child(node: Node):
        """
        1. If the given node has no children, return this node.
        2. If we find a child that has never been visited, return this node.
        3. Otherwise, choose the child with the largest UCT value.
        """
        selected = node
        if selected.is_leaf():
            return selected

        max_uct = 0
        for child in node.children:
            if child.visits == 0:
                return child

            this_uct = child.sp_uct
            if this_uct > max_uct:
                max_uct = this_uct
                selected = child

        return selected

    @staticmethod
    def _find_children(node: Node) -> List[Node]:
        """ Find all children associated with the current node. """
        children = []
        for state in node.state.get_possible_states():
            children.append(Node(state))
            gm.Visual.handle_state(
                state, f'EXPANSION_{str(state.move_taken_from_parent)}_FROM_{str(node.state)}'
            )

        return children

    def _selection(self) -> Node:
        """
        Traverse from our root to a leaf node. When a node has a child, choose according to the policy defined
        in _pick_child. When we have reached a leaf node, return that node.
        """
        selected = self.root
        while not selected.is_leaf():
            selected = self._pick_child(selected)

        return selected

    def _expansion(self, leaf_node: Node):
        """
        1. If the game is in a terminal state, exit and return None.
        2. If our leaf currently has no visits, return this leaf.
        3. Otherwise, expand our leaf node to include more children. Do not include ourself as a child.
        """
        if not leaf_node.is_leaf():
            logger.error(f'Error: the following node {leaf_node} is not a leaf.')
            raise RuntimeError(f'Error:the following node {leaf_node} is not a leaf.')

        if leaf_node.state.is_terminal():
            logger.info('Game has reached a terminal state.')
            logger.debug(f'Current game state: \n{leaf_node.state}')
            return None

        elif leaf_node.visits == 0:
            return leaf_node

        else:
            for child in self._find_children(leaf_node):
                if child.state != leaf_node.state:
                    leaf_node.add_child(child)

            child = self._pick_child(leaf_node)
            logger.debug(f'Expanded the following node: {child}')
            return child

    def _simulation(self, node: Node, i: int):
        """
        1. Randomly traverse our tree from the given game state until we reach a terminal state OR until we reach our
        simulation bound.
        2. Return the heuristic value associated with this state if the game has not been won. Otherwise, return a
        solution instance.
        """
        current_state = node.state
        simulated_moves = deque()
        count = 0

        # Traverse to a terminal state.
        while not current_state.is_terminal() and count < self.simulation_bound:
            current_state = gm.Evaluation.make_random_move(current_state)
            gm.Visual.handle_state(current_state, f'SIMULATION_{i}')
            simulated_moves.append(current_state.move_taken_from_parent)
            count = count + 1

        if not current_state.is_solved():
            return self.heuristic_f(current_state)
        else:
            return Solution(node, simulated_moves, i + 1)

    def _back_propagation(self, node: Node, h: float):
        """ From the given node with a terminal state, propagate all of results up to the root. """
        root_h = self.heuristic_f(self.root.state)
        corrected_h = self.heuristic_correction_f(h, root_h)

        current_node = node
        current_node.h_sum += corrected_h
        current_node.h_sum_sq += corrected_h ** 2
        current_node.visits += 1
        current_node.sp_uct = self._calculate_uct(current_node)

        while current_node.is_descendant():
            current_node = current_node.parent
            current_node.h_sum += corrected_h
            current_node.h_sum_sq += corrected_h ** 2
            current_node.visits += 1
            current_node.sp_uct = self._calculate_uct(current_node)

    def _calculate_uct(self, node: Node):
        """
        - Compute the UCT (upper confidence bounds applied to trees) value associated with a given node. This value is:
        (the win ratio of a child) + (exploration constant) * sqrt(log(parent visits) / child visits)
        - The first term corresponds to exploitation, while the second corresponds to exploration.
        - An additional third term comes from the paper, which represents an uncertainty in the child node that hasn't
        been explored as thoroughly.
        """
        c = self.exploration_c
        w = node.h_sum
        n = node.visits
        if not node.is_descendant():
            t = node.visits
        else:
            t = node.parent.visits
        uct = w / n + c * np.sqrt(np.log(t) / n)
        logger.debug(f'Win ratio of node {node} is computed to be: {w / n}')
        logger.debug(f'UCT of node {node} is computed to be: {uct}')

        sum_sq = node.h_sum_sq
        d = self.uncertainty_d
        modif = np.sqrt((sum_sq - n * (w / n)**2 + d) / n)
        logger.debug(f'Additional term of node {node} is computed to be: {modif}')

        resultant = uct + modif
        logger.debug(f'Resulting UCT of node {node} is: {resultant}')
        return resultant
