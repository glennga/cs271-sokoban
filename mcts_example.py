# import mctsnode as nd
# import numpy as np
# import singplayermcts as mc
# import game_model_old as game
#
# if __name__ == '__main__':
#     rootState = game.createGame("resources/sokoban03.txt")
#
#     root = nd.Node(rootState)
#     x = mc.MCTS(root)
#     x.run(1000)

import single_player_mcts as mc
import game_model as gm

if __name__ == '__main__':
    root_state = gm.GameState.build('resources/sokoban01.txt')
    root_node = mc.Node(root_state)
    x = mc.MCTS(root_node, gm.GameModel.heuristic_3, 20)
    x.run(1000)
    x.get_solution()
