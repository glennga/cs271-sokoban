import collections


def generate_graph(game_board):
    G = {}
    white_space_coordinates = set()
    box_coordinates = set()
    target_coordinates = set()
    agent_coordinate = (0, 0)

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == "#":
                pass
            else:
                if game_board[i][j] == " ":
                    white_space_coordinates.add((i, j))
                elif game_board[i][j] == ".":
                    target_coordinates.add((i, j))

                elif game_board[i][j] == "$":
                    box_coordinates.add((i, j))

                else:
                    agent_coordinate = (i, j)

                children = []
                if j - 1 > 0 and game_board[i][j - 1] != "#":
                    children.append((i, j - 1))
                elif j + 1 < len(game_board[i]) and game_board[i][j + 1] != "#":
                    children.append((i, j + 1))
                elif i - 1 > 0 and game_board[i - 1][j] != "#":
                    children.append((i, j))

                elif i + 1 < len(game_board) and game_board[i][j + 1] != "#":
                    children.append((i, j))

                G[(i, j)] = children

    return (G, white_space_coordinates, box_coordinates, target_coordinates, agent_coordinate)




def check_box_target_feasible(box_location, target_location, agent_location, G):
    b_x = box_location[0]
    b_y = box_location[1]
    movable_squares = G[1].union(G[3]).union(G[4])
    if reachable(box_location, target_location, G):
        #find children of box_location
        children = G[0][box_location]
        
        if (b_x -1, b_y) in children and (b_x + 1, b_y) in movable_squares:
            if reachable(agent_location, (b_x + 1, b_y), G):
                return 1

        elif (b_x +1, b_y) in children and (b_x - 1, b_y) in movable_squares:
            if reachable(agent_location, (b_x -1, b_y), G):
                return 1
            
        elif (b_x, b_y -1 ) in children and (b_x, b_y+1) in movable_squares:
            if reachable(agent_location, (b_x, b_y + 1), G):
                return 1
    
        elif (b_x, b_y +1) in children and (b_x, b_y -1) in movable_squares:
            if reachable(agent_location, (b_x, b_y -1), G):
                return 1

        else:
            return 0
    else:
        return 0
    #find corresponding squaree agent has to push
    #start bfs from box_location to target_location

    #if reachable look at all children of box and find corresponding locations for agents
    #check if agent is reachable to that square





def reachable(a,b, G):
    explored = set()

    queue = collections.deque([])
    
    queue.append(a)

    while(len(queue) > 0):
        node = queue.popleft()
        if node != a and node in G[2]:
            pass
        else:
            children = G[0][node]
            for child in children:
                if child not in explored:
                    queue.append(child)

        explored.add(node)

    if b in explored:
        return 1

    else:
        return 0
        



def check_dead_state(game_board):
    G = generate_graph(game_board)


    box_coordinates = G[2]
    target_coordinates = G[3]
    agent_coordinate = G[4]

    temp = []
    for box in box_coordinates:
        for target in target_coordinates:
            if check_box_target_feasible(box, target, agent_coordinate, G):
                temp.append(1)
                break


    if sum(temp) == len(box_coordinates):
        return 0

    else:
        return 1


#G = [['#', '#', '#', '#', '#', '#', '#', '#'], ['#', '.', '$', '#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', '@', ' ', '$', '#'], ['#', ' ', ' ', ' ', '#', ' ', '#', '#'], ['#', '#', ' ', '#', '$', ' ', '.', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '.', '#', ' ', ' ', '#'], ['#', '#', '#', '#', '#', '#', '#', '#']]

G = [['#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#'], ['#', ' ', ' ', '$', '#'], ['#', ' ', ' ', '@', '#'], ['#', '#', '#', '#', '#']]



print(check_dead_state(G))
