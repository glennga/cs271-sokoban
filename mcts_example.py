import single_player_mcts as mc
import game_model as gm

if __name__ == '__main__':
    root_state = gm.State.build('resources/from_class/sokoban01.txt')
    root_node = mc.Node(root_state)
    x = mc.MCTS(**{
        'root': root_node,
        'heuristic_f': gm.Evaluation.heuristic_3,
        'simulation_bound': 250,
        'exploration_c': 0.5,
        'uncertainty_d': 50.0,
        'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
    })

    # Visualize our run.
    gm.Visual.start_instance()
    solution = x.run(10000)

    # Print our solution.
    gm.Visual.kill_instance()
    print(solution)
