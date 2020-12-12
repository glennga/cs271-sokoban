import unittest
import game_model as gm
import mctsnode as nd
import singplayermcts as mc


class TestMCTS(unittest.TestCase):
    def test_sokoban00(self):
        """
        ###        ###
        #@#        # #
        #$#  --->  #@#
        #.#        #$#
        ###        ###
        """
        m0 = gm.createGame('resources/sokoban00.txt')
        root = nd.Node(m0)
        x0 = mc.MCTS(root)
        x0.run()

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
        m0 = gm.createGame('resources/sokoban01.txt')
        root = nd.Node(m0)
        x0 = mc.MCTS(root)
        x0.run()

    def test_sokoban02(self):
        """
        ####        ####
        # .#        # $#
        # $#  --->  # @#
        #@ #        #  #
        ####        ####
        """
        m0 = gm.createGame('resources/sokoban02.txt')
        root = nd.Node(m0)
        x0 = mc.MCTS(root)
        x0.run()

    def test_sokoban03(self):
        """
        ######        ######
        # .. #        # $$ #
        # $$ #        #  @ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        m0 = gm.createGame('resources/sokoban03.txt')
        root = nd.Node(m0)
        x0 = mc.MCTS(root)
        x0.run()

    def test_other_examples(self):
        """ Test all other examples. """
        pass
