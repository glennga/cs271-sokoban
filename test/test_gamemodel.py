import unittest
import game_model as gm

class TestGameModel(unittest.TestCase):
    def test_sokoban00(self):
        """
        ###        ###
        #@#        # #
        #$#  --->  #@#
        #.#        #$#
        ###        ###
        """
        solve_box_1 = [gm.Game.Move.DOWN]

        m0 = gm.createGame('resources/sokoban00.txt')
        self.assertEqual(len(gm.legal_moves(m0)), 1)
        self.assertEqual(gm.legal_moves(m0)[0], solve_box_1[0])
        self.assertFalse(gm.solved(m0))

        m1 = gm.makeMove(m0, solve_box_1[0])
        self.assertTrue(gm.solved(m1))

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
        solve_box_1 = [gm.Game.Move.LEFT, gm.Game.Move.UP, gm.Game.Move.LEFT, gm.Game.Move.LEFT, gm.Game.Move.RIGHT,
                       gm.Game.Move.UP, gm.Game.Move.RIGHT]
        solve_box_2 = [gm.Game.Move.UP, gm.Game.Move.UP, gm.Game.Move.LEFT, gm.Game.Move.LEFT, gm.Game.Move.LEFT,
                       gm.Game.Move.DOWN, gm.Game.Move.LEFT, gm.Game.Move.UP]
        solve_box_3 = [gm.Game.Move.DOWN, gm.Game.Move.RIGHT, gm.Game.Move.DOWN, gm.Game.Move.DOWN, gm.Game.Move.LEFT,
                       gm.Game.Move.DOWN, gm.Game.Move.RIGHT]

        m0 = gm.createGame('resources/sokoban01.txt')
        self.assertEqual(len(gm.legal_moves(m0)), 2)
        self.assertIn(gm.Game.Move.LEFT, gm.legal_moves(m0))
        self.assertIn(gm.Game.Move.UP, gm.legal_moves(m0))
        self.assertFalse(gm.solved(m0))
        self.assertEqual(len(set(m0.Boxes).difference(set(m0.storLocs))), 3)

        mi = m0
        for move in solve_box_1:
            mi = gm.makeMove(mi, move)
        self.assertEqual(len(set(mi.Boxes).difference(set(mi.storLocs))), 2)

        for move in solve_box_2:
            mi = gm.makeMove(mi, move)
        self.assertEqual(len(set(mi.Boxes).difference(set(mi.storLocs))), 1)

        for move in solve_box_3:
            mi = gm.makeMove(mi, move)
        self.assertTrue(gm.solved(mi))

    def test_sokoban02(self):
        """
        ####        ####
        # .#        # $#
        # $#  --->  # @#
        #@ #        #  #
        ####        ####
        """
        solve_box_1 = [gm.Game.Move.RIGHT, gm.Game.Move.UP]

        m0 = gm.createGame('resources/sokoban02.txt')
        self.assertEqual(len(gm.legal_moves(m0)), 2)
        self.assertIn(gm.Game.Move.UP, gm.legal_moves(m0))
        self.assertIn(gm.Game.Move.RIGHT, gm.legal_moves(m0))
        self.assertFalse(gm.solved(m0))

        m1 = gm.makeMove(m0, solve_box_1[0])
        m2 = gm.makeMove(m1, solve_box_1[1])
        self.assertTrue(gm.solved(m2))

    def test_sokoban03(self):
        """
        ######        ######
        # .. #        # $$ #
        # $$ #        #  @ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        solve_box_1 = [gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.UP]
        solve_box_2 = [gm.Game.Move.DOWN, gm.Game.Move.RIGHT, gm.Game.Move.UP]

        m0 = gm.createGame('resources/sokoban03.txt')
        self.assertEqual(len(gm.legal_moves(m0)), 2)
        self.assertIn(gm.Game.Move.RIGHT, gm.legal_moves(m0))
        self.assertIn(gm.Game.Move.UP, gm.legal_moves(m0))
        self.assertFalse(gm.solved(m0))
        self.assertEqual(len(set(m0.Boxes).difference(set(m0.storLocs))), 2)

        mi = m0
        for move in solve_box_1:
            mi = gm.makeMove(mi, move)
        self.assertEqual(len(set(mi.Boxes).difference(set(mi.storLocs))), 1)

        for move in solve_box_2:
            mi = gm.makeMove(mi, move)
        self.assertTrue(gm.solved(mi))

    def test_badcorner(self):
        """ (in all four corners)
        ######        ######
        # .. #        # .@$#
        # $$ #        #  $ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        fail_upleft = [gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.UP,
                       gm.Game.Move.LEFT]
        fail_upright = [gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.RIGHT, gm.Game.Move.UP, gm.Game.Move.LEFT,
                        gm.Game.Move.UP, gm.Game.Move.RIGHT]
        fail_bottomleft = [gm.Game.Move.UP, gm.Game.Move.UP, gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.DOWN,
                           gm.Game.Move.DOWN, gm.Game.Move.RIGHT, gm.Game.Move.DOWN, gm.Game.Move.LEFT]
        fail_bottomright = [gm.Game.Move.UP, gm.Game.Move.UP, gm.Game.Move.UP, gm.Game.Move.RIGHT, gm.Game.Move.RIGHT,
                            gm.Game.Move.DOWN, gm.Game.Move.DOWN, gm.Game.Move.LEFT, gm.Game.Move.DOWN,
                            gm.Game.Move.RIGHT]

        mi = gm.createGame('resources/sokoban03.txt')
        for move in fail_upleft:
            mi = gm.makeMove(mi, move)
        self.assertFalse(gm.solved(mi))
        self.assertTrue(any(gm.inBadCorner(b, mi) for b in mi.Boxes))

        mi = gm.createGame('resources/sokoban03.txt')
        for move in fail_upright:
            mi = gm.makeMove(mi, move)
        self.assertFalse(gm.solved(mi))
        self.assertTrue(any(gm.inBadCorner(b, mi) for b in mi.Boxes))

        mi = gm.createGame('resources/sokoban03.txt')
        for move in fail_bottomleft:
            mi = gm.makeMove(mi, move)
        self.assertFalse(gm.solved(mi))
        self.assertTrue(any(gm.inBadCorner(b, mi) for b in mi.Boxes))

        mi = gm.createGame('resources/sokoban03.txt')
        for move in fail_bottomright:
            mi = gm.makeMove(mi, move)
        self.assertFalse(gm.solved(mi))
        self.assertTrue(any(gm.inBadCorner(b, mi) for b in mi.Boxes))


if __name__ == '__main__':
    unittest.main()
