import single_player_mcts as mc
import game_model as gm
import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    input_file = 'resources/from_class/benchmark/sokoban02.txt'
    mcts_params = {
        'heuristic_f': gm.Evaluation.heuristic_3,
        'simulation_bound': 300,
        'exploration_c': 0.5,
        'uncertainty_d': 50.0,
        'heuristic_correction_f': gm.Evaluation.heuristic_3_correction
    }
    logger.info(f'Starting new run for input file: {input_file}.')
    logger.info(f'MCTS parameters: {mcts_params}')

    root_state = gm.State.build(input_file)
    root_node = mc.Node(root_state)
    x = mc.MCTS(**{**mcts_params, **{'root': root_node}})

    # Visualize our run.
    gm.Visual.start_instance()
    solution = x.run(10000)

    # Print our solution.
    gm.Visual.kill_instance()
    logger.info(f'Solution: {solution}')
