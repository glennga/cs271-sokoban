import unittest
import game_model as gm
import single_player_mcts as mc


class TestMCTS(unittest.TestCase):
    def test_sokoban00(self):
        """
        ###        ###
        #@#        # #
        #$#  --->  #@#
        #.#        #$#
        ###        ###
        """
        root_state = gm.GameState.build('resources/sokoban00.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.GameModel.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.GameModel.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())

    def test_sokoban01(self):
        """
        ########        ########
        #. #   #        #$ #   #
        #  $   #        #      #
        #   # ##        #   # ##
        ## # $.#  --->  ## #  $#
        #   $  #        #      #
        #  .# @#        # @$#  #
        ########        ########
        """
        root_state = gm.GameState.build('resources/sokoban01.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.GameModel.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.GameModel.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())

    def test_sokoban02(self):
        """
        ####        ####
        # .#        # $#
        # $#  --->  # @#
        #@ #        #  #
        ####        ####
        """
        root_state = gm.GameState.build('resources/sokoban02.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.GameModel.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.GameModel.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())

    def test_sokoban03(self):
        """
        ######        ######
        # .. #        # $$ #
        # $$ #        #  @ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        root_state = gm.GameState.build('resources/sokoban03.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.GameModel.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.GameModel.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())

    def test_other_examples(self):
        """ Test all other examples. """
        pass
