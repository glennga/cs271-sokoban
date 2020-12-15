import __init__
improt mctsnode as nd
import numpy as np
import game_model as game
import logging




logger = logging.getLogger(__name__)


class A_star:
    def __init__(self, Node):
        self.root = Node
        heuristic_value = game.Evaluation.heuristic_2(Node.state)
        self.pq = [(Node, Node.heuristic)]
        self.explored = set()
        self.parent_cost_dict = {}
        #self.node_cost_dict = {}
    
        self.parent_cost_dict[self.root] = ["BIG DADDY", 0]
    

    #select unexplored node with cheapest cost
    def selection(self):
        expanded_list = []
        for i in range(len(self.pq)):
            expanded_list.append((self.pq[i][0], self.pq[i][1], i))

        sorted_list = sorted(expanded_list, key = lambda x: x[1])
        index = sorted_list[0][2]

        self.pq = expanded_list[0:index] + expanded_list[index+1:]

        return sorted_list[0][0]

    #explore node, add node to explored set, and children to queue
    def explore(self, node):
        next_states = game.possibleStates(Node.state)

        children = []

        for state in nextStates:
            ChildNode = nd.Node(state)

                heuristic_score = game.Evaluation.heuristic_2(state))
            if ChildNode not in self.explored:
                self.pq.append((ChildNode, self.parent_cost_dict[childNode] + heuristic_score)) 
                self.parent_cost_dict[ChildNode] = [node, self.parent_cost_dict[node] + heuristic_score]        

            else:
                if self.parent_cost_dict[node] + heurist

    def run(self, iters = 4000):
        while len(explored) <= 4000:
            node = self.selection()
            #print(game_board) For debugging
            if final_state(node):
                print("Solution Found")
            else:
                self.explore(node)

            #pick unexplored node with cheapest cost
            #check if its goal state
                #if goal state return solution
                #else add children to priority queue

            #add node to explored

            #do something

        


        

