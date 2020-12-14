


import collections
#if child is a box add it but don't take any children of boxes
#if child is wal ignore


def generate_graph(game_board):
    G = {}
    white_space_coordinates = set()
    box_coordinates = set()
    target_coordinates = set()
    agent_coordinate = (0,0)

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == "#":
                pass
            else:
                if game_board[i][j] == " ":
                    white_space_coordinates.add((i,j))
                elif game_board[i][j] == ".":
                    target_coordinates.add((i,j))

                elif game_baord[i][j] == "$":
                    box_coordinates.add((i,j))

                else:
                    agent_coordinate = (i,j)


                children = []
                if j-1 > 0 and game_board[i][j-1] != "#":
                    children.append((i, j-1))
                elif j+1 < len(game_board[i]) and game_board[i][j+1] != "#":
                    children.append((i,j + 1))
                elif i-1 > 0 and game_board[i-1][j] != "#":
                    children.append((i,j))

                elif i+1 < len(game_board) and game_board[i][j+1] != "#":
                    children.append((i,j))

                G[(i,j)] = children


    return (G, white_space_coordinates, box_coordinates, target_coordinates, agent_coordinate)

def modified_bfs(G):

    agent_coordinate = G[4])
    connected_components = []
    
    explored = set()
    

    queue = collections.deque([])

    cc = []
    while len(explored) < len(G[1]) + len(G[2]) + len(G[3]) + 1:
        if len(queue) == 0:
            connected_components.append(cc)
            cc = []
            l = G[1].union(G[3]) - explored
            l = list(l)
            queue.append(l[0])
            pass
            #add connected component and create new one
            #pick new non_target and add start bfs from there.

        else:
            node = queue.popleft()
            cc.append(node)
            

            if node in box_coordinates:
                pass
            else:
                for children in GG[0][node]:
                    if children not in explored:
                        queue.append(children)

            explored.add(node)




    queue.append(agent_coordinate)

    return connected_components



def check_dead_state(game_board):
    G = generate_graph(game_board)

    connected_components = modified_bfs(G)

    if len(connected_components) > 1:
        return 0

    else:
        return 1


