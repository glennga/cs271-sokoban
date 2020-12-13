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
    x = mc.MCTS(**{
        'root': root_node,
        'heuristic_f': gm.GameModel.heuristic_3,
        'simulation_bound': 1000,
        'exploration_c': 0.5,
        'uncertainty_d': 50.0,
        'heuristic_correction_f': gm.GameModel.heuristic_3_correction
    })

    gm.GameVisualize.start_instance()
    x.run(1000)

    gm.GameVisualize.kill_instance()
    # x.get_solution()
