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
        solve_box_1 = [gm.Action.DOWN]

        m0 = gm.State.build('resources/from_class/sokoban00.txt')
        self.assertEqual(len(m0._legal_moves()), 1)
        self.assertEqual(m0._legal_moves()[0], solve_box_1[0])
        self.assertFalse(m0.is_solved())

        m1 = m0.move(solve_box_1[0])
        self.assertTrue(m1.is_solved())

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
        solve_box_1 = [gm.Action.LEFT, gm.Action.UP, gm.Action.LEFT, gm.Action.LEFT, gm.Action.RIGHT,
                       gm.Action.UP, gm.Action.RIGHT]
        solve_box_2 = [gm.Action.UP, gm.Action.UP, gm.Action.LEFT, gm.Action.LEFT, gm.Action.LEFT,
                       gm.Action.DOWN, gm.Action.LEFT, gm.Action.UP]
        solve_box_3 = [gm.Action.DOWN, gm.Action.RIGHT, gm.Action.DOWN, gm.Action.DOWN, gm.Action.LEFT,
                       gm.Action.DOWN, gm.Action.RIGHT]

        m0 = gm.State.build('resources/from_class/sokoban01.txt')
        self.assertEqual(len(m0._legal_moves()), 2)
        self.assertIn(gm.Action.LEFT, m0._legal_moves())
        self.assertIn(gm.Action.UP, m0._legal_moves())
        self.assertFalse(m0.is_solved())
        self.assertEqual(len(set(m0.boxes).difference(set(m0.storage_locations))), 3)

        mi = m0
        for action in solve_box_1:
            mi = mi.move(action)
        self.assertEqual(len(set(mi.boxes).difference(set(mi.storage_locations))), 2)

        for action in solve_box_2:
            mi = mi.move(action)
        self.assertEqual(len(set(mi.boxes).difference(set(mi.storage_locations))), 1)

        for action in solve_box_3:
            mi = mi.move(action)
        self.assertTrue(mi.is_solved())

    def test_sokoban02(self):
        """
        ####        ####
        # .#        # $#
        # $#  --->  # @#
        #@ #        #  #
        ####        ####
        """
        solve_box_1 = [gm.Action.RIGHT, gm.Action.UP]

        m0 = gm.State.build('resources/from_class/sokoban02.txt')
        self.assertEqual(len(m0._legal_moves()), 2)
        self.assertIn(gm.Action.UP, m0._legal_moves())
        self.assertIn(gm.Action.RIGHT, m0._legal_moves())
        self.assertFalse(m0.is_solved())

        m1 = m0.move(solve_box_1[0])
        m2 = m1.move(solve_box_1[1])
        self.assertTrue(m2.is_solved())

    def test_sokoban03(self):
        """
        ######        ######
        # .. #        # $$ #
        # $$ #        #  @ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        solve_box_1 = [gm.Action.UP, gm.Action.RIGHT, gm.Action.UP]
        solve_box_2 = [gm.Action.DOWN, gm.Action.RIGHT, gm.Action.UP]

        m0 = gm.State.build('resources/from_class/sokoban03.txt')
        self.assertEqual(len(m0._legal_moves()), 2)
        self.assertIn(gm.Action.RIGHT, m0._legal_moves())
        self.assertIn(gm.Action.UP, m0._legal_moves())
        self.assertFalse(m0.is_solved())
        self.assertEqual(len(set(m0.boxes).difference(set(m0.storage_locations))), 2)

        mi = m0
        for action in solve_box_1:
            mi = mi.move(action)
        self.assertEqual(len(set(mi.boxes).difference(set(mi.storage_locations))), 1)

        for action in solve_box_2:
            mi = mi.move(action)
        self.assertTrue(mi.is_solved())

    def test_bad_corner(self):
        """ (in all four corners)
        ######        ######
        # .. #        # .@$#
        # $$ #        #  $ #
        #    #  --->  #    #
        #@   #        #    #
        ######        ######
        """
        fail_upleft = [gm.Action.UP, gm.Action.RIGHT, gm.Action.UP, gm.Action.RIGHT, gm.Action.UP,
                       gm.Action.LEFT]
        fail_upright = [gm.Action.UP, gm.Action.RIGHT, gm.Action.RIGHT, gm.Action.UP, gm.Action.LEFT,
                        gm.Action.UP, gm.Action.RIGHT]
        fail_bottomleft = [gm.Action.UP, gm.Action.UP, gm.Action.UP, gm.Action.RIGHT, gm.Action.DOWN,
                           gm.Action.DOWN, gm.Action.RIGHT, gm.Action.DOWN, gm.Action.LEFT]
        fail_bottomright = [gm.Action.UP, gm.Action.UP, gm.Action.UP, gm.Action.RIGHT, gm.Action.RIGHT,
                            gm.Action.DOWN, gm.Action.DOWN, gm.Action.LEFT, gm.Action.DOWN,
                            gm.Action.RIGHT]

        mi = gm.State.build('resources/from_class/sokoban03.txt')
        for action in fail_upleft:
            mi = mi.move(action)
        self.assertFalse(mi.is_solved())
        self.assertTrue(any(mi.in_bad_corner(b) for b in mi.boxes))

        mi = gm.State.build('resources/from_class/sokoban03.txt')
        for action in fail_upright:
            mi = mi.move(action)
        self.assertFalse(mi.is_solved())
        self.assertTrue(any(mi.in_bad_corner(b) for b in mi.boxes))

        mi = gm.State.build('resources/from_class/sokoban03.txt')
        for action in fail_bottomleft:
            mi = mi.move(action)
        self.assertFalse(mi.is_solved())
        self.assertTrue(any(mi.in_bad_corner(b) for b in mi.boxes))

        mi = gm.State.build('resources/from_class/sokoban03.txt')
        for action in fail_bottomright:
            mi = mi.move(action)
        self.assertFalse(mi.is_solved())
        self.assertTrue(any(mi.in_bad_corner(b) for b in mi.boxes))


if __name__ == '__main__':
    unittest.main()
