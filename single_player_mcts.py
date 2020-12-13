from __future__ import annotations
from typing import List
from typing import Callable

import __init__
import game_model as gm
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, state: gm.GameState):
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


class MCTS:
    def __init__(self, root: Node, heuristic_f: Callable, simulation_bound: int = 20, exploration_c: float = 0.5,
                 uncertainty_d: float = 50, heuristic_correction_f: Callable = lambda h, root_h: h):
        self.root = root
        self.simulation_bound = simulation_bound
        self.exploration_c = exploration_c
        self.uncertainty_d = uncertainty_d

        self.heuristic_f = heuristic_f
        self.heuristic_correction_f = heuristic_correction_f

    def run(self, iterations: int):
        """
        1. For the given amount of iterations...
        2. Select a leaf node and expand it.
        3. If we have not reached a terminal state, then simulate and backpropagate.
        4. Otherwise, backpropagate our result.
        """
        for i in range(iterations):
            logger.debug(f'Starting iteration {i}.')
            x = self._selection()
            y = self._expansion(x)

            if y is not None:
                h, w = self._simulation(y, i)
                self._back_propagation(y, h, w)
            else:
                h = self.heuristic_f(x.state)
                w = x.state.is_solved()
                self._back_propagation(x, h, w)

        logger.info('Search complete.')

    def get_solution(self) -> str:
        """ Traverse our root to a terminal state, choosing the most "winning" nodes along the way. """
        logger.info('Now traversing our tree to find the solution.')
        output_str = ''

        current_node = self.root
        i = 1  # Current step count.
        logger.debug('0 - Starting state.')

        previous_move, current_move_count = None, 1
        while len(current_node.children) != 0:
            current_node = max(current_node.children, key=lambda x: x.h_sum)
            current_move = current_node.state.move_taken_from_parent

            logger.debug(f'{i} - Taking move {str(current_move)}.')
            if previous_move != current_move:
                output_str = output_str + f'{current_move_count} {str(current_node.state.move_taken_from_parent)} '
                current_move_count = 1
            else:
                current_move_count = current_move_count + 1
            previous_move = current_move
            i = i + 1

        if current_move_count > 1:  # Account for tail.
            output_str = output_str + f'{current_move_count} {str(current_node.state.move_taken_from_parent)} '
        logger.info(f'In project format: {output_str}.')
        return output_str

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
            gm.GameVisualize.handle_state(
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
        2. Return a) the heuristic value associated with this state, and b) if the terminal state is a win or not.
        """
        current_state = node.state
        count = 0

        while not current_state.is_terminal() and count < self.simulation_bound:
            current_state = gm.GameModel.make_random_move(current_state)
            count = count + 1
            gm.GameVisualize.handle_state(current_state, f'SIMULATION_{i}_FROM_{str(node.state.current_location)}')

        return self.heuristic_f(current_state), (1 if current_state.is_solved() else 0)

    def _back_propagation(self, node: Node, h: float, w: int):
        """ From the given node with a terminal state, propagate all of results up to the root. """
        root_h = self.heuristic_f(self.root.state)
        corrected_h = self.heuristic_correction_f(h, root_h)
        corrected_h = corrected_h if w == 0 else 1  # Default to 1 if we have won.

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
