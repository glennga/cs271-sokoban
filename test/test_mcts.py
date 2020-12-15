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
        root_state = gm.State.build('resources/from_class/sokoban00.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.Evaluation.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
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
        root_state = gm.State.build('resources/from_class/sokoban01.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.Evaluation.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
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
        root_state = gm.State.build('resources/from_class/sokoban02.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.Evaluation.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
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
        root_state = gm.State.build('resources/from_class/sokoban03.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.Evaluation.heuristic_3,
            'simulation_bound': 200,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())

    def test_xsokoban01(self):
        """
        ######        ######
        # .. #        # $$ #
        # $$ #        #  @ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        root_state = gm.State.build('resources/from_outside/xsokoban01_formatted.txt')
        root_node = mc.Node(root_state)
        x = mc.MCTS(**{
            'root': root_node,
            'heuristic_f': gm.Evaluation.heuristic_3,
            'simulation_bound': 1000,
            'exploration_c': 0.5,
            'uncertainty_d': 50.0,
            'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
        })
        solution_sequence = x.run(10000)
        self.assertIsInstance(solution_sequence, mc.Solution)

        current_state = root_state
        for action in solution_sequence:
            current_state = current_state.move(action)

        self.assertTrue(current_state.is_solved())
