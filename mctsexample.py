import mctsnode as nd
import numpy as np 
import singplayermcts as mc 
import game_model as game


rootState = game.createGame("sokoban03.txt")

root = nd.Node(rootState)

x = mc.MCTS(root, True)

x.run()