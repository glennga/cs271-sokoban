import mctsnode as nd
import numpy as np 
import singplayermcts as mc 
import game_model as game

if __name__ == '__main__':
    rootState = game.createGame("resources/sokoban01.txt")

    root = nd.Node(rootState)
    x = mc.MCTS(root)

    x.run()