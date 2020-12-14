
for i in range(1, 91):
    file_header = "xsokoban"
    number = ""
    if i < 10:
        number = "0" + str(i)
    else:
        number = str(i)

    file_name = file_header + number + ".xsb"


    file_r = open(file_name, "r")

    game_board = []


    line_ctr = 1
    for line in file_r:
        c = line.rstrip()
        row = []
        for char in c:
            row.append(char)
        #row = line.split("")
        game_board.append(row)
        line_ctr += 1

    file_r.close()

    H = 0
     
    V = len(game_board)

    for i in range(V):
        if len(game_board[i]) > H:
            H = len(game_board[i])


    wall_squares = ""
    wall_ctr = 0

    target_squares = ""
    target_ctr = 0

    box_squares = ""
    box_ctr = 0

    agent_square = ""


    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == "#":
                wall_squares += " " + str(i+1) + " " + str(j+1)
                wall_ctr += 1

            elif game_board[i][j] == "@":
                agent_square = str(i+1) + " " + str(j+1)

            elif game_board[i][j] == ".":
                target_squares += " " +  str(i+1) + " " + str(j+1)
                target_ctr += 1

            elif game_board[i][j] == "$":
                box_squares +=  " " + str(i+1) + " " + str(j+1)
                box_ctr += 1
            

    wall_str = str(wall_ctr) + wall_squares
    box_str = str(box_ctr) + box_squares
    target_str = str(target_ctr) + target_squares


    file_w = open(file_header + number  + "_formated.txt", "w")


    file_w.write(str(H) + " " + str(V) + "\n")
    file_w.write(wall_str + "\n")
    file_w.write(box_str + "\n")
    file_w.write(target_str + "\n")
#file_w.write("Hi\n")
    file_w.write(agent_square + "\n")
    file_w.close()


    print(game_board)

    print(agent_square)
