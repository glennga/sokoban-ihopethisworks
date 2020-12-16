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
                if j - 1 >= 0 and game_board[i][j - 1] != "#":
                    children.append((i, j - 1))
                if j + 1 < len(game_board[i]) and game_board[i][j + 1] != "#":
                    children.append((i, j + 1))
                if i - 1 >= 0 and game_board[i - 1][j] != "#":
                    children.append((i-1, j))

                if i + 1 < len(game_board) and game_board[i+1][j] != "#":
                    children.append((i+1, j))

                G[(i, j)] = children

    return (G, white_space_coordinates, box_coordinates, target_coordinates, agent_coordinate)




def check_box_target_feasible(box_location, target_location, agent_location, G):
    b_x = box_location[0]
    b_y = box_location[1]
    movable_squares = G[1].union(G[3]).union(set([G[4]]))
    #print("movable", G[1], G[3], G[4])
    if reachable(box_location, target_location, G):
        #find children of box_location
        children = G[0][box_location]
        #print("child", children) 
        #print(movable_squares)
        if (b_x -1, b_y) in children and (b_x + 1, b_y) in movable_squares and (b_x-1, b_y) not in G[2]:
            #print((b_x -1, b_y),"->", (b_x +1, b_y))
            if reachable(agent_location, (b_x + 1, b_y), G):
                return 1

        if (b_x +1, b_y) in children and (b_x - 1, b_y) in movable_squares and (b_x+1, b_y) not in G[2]:
            #print((b_x +1, b_y),"->", (b_x -1, b_y))
            if reachable(agent_location, (b_x -1, b_y), G):
                return 1
            
        if (b_x, b_y -1 ) in children and (b_x, b_y+1) in movable_squares and (b_x, b_y-1) not in G[2]:
            #print((b_x, b_y-1),"->", (b_x , b_y+1))
            if reachable(agent_location, (b_x, b_y + 1), G):
                return 1
    
        if (b_x, b_y +1) in children and (b_x, b_y -1) in movable_squares and (b_x, b_y+1) not in G[2]:
            #print((b_x, b_y+1),"->", (b_x , b_y-1))
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
    #print(G[4])
    #print(a,b)

    if a not in G[0] or b not in G[0]:
        #print(a,b,0, "not in graph")
        return False

    explored = set()

    queue = collections.deque([])
    
    queue.append(a)
    #print(G[1])
    #print(G)
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


    #print(explored)

    if b in explored:
        #print(a,b, 1)
        return 1

    else:
        #print(a,b,0)
        return 0
        





def check_dead_state_static(game_board):
    #print("-----")
    #wrapper(game_board)
    #print("-----")
    G = generate_graph(game_board)  

    #print(G)

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
        return False

    else:
        return True


def copy_list_by_value(l):
    a = []
    for i in l:
        t = []
        for j in i:
            if j == " ":
                t.append(" ")
            elif j == "#":
                t.append("#")
            elif j == "$":
                t.append("$")
            elif j == ".":
                t.append(".")
            elif j == "@":
                t.append("@")
        a.append(t)

    return a


def is_dead_state(game_board):
    c_game_board = copy_list_by_value(game_board)
    if check_dead_state_static(game_board):
        G = generate_graph(game_board)

        #print(game_board)
        #new_board1 = copy_list_by_value(game_board)
        #new_board2 = copy_list_by_value(game_board)
        #new_board3 = copy_list_by_value(game_board)
        #new_board4 = copy_list_by_value(game_board)

        #print(new_board1, new_board2, new_board3, new_board4)

        for (b_x, b_y) in G[2]:
            #new_board1 = copy_list_by_value(game_board)
            #new_board2 = copy_list_by_value(game_board)
            #new_board3 = copy_list_by_value(game_board)
            #new_board4 = copy_list_by_value(game_board)
            print((b_x, b_y), "box")
            #print(G[1].union(G[3]))
            #print((b_x+1, b_y) in G[1].union(G[3]))
            ctr = 0
            while (b_x+1, b_y)  in G[1].union(G[3]) and reachable(G[4],(b_x-ctr-1, b_y), G) and (b_x-ctr-1, b_y) not in G[2]:
                #print("hi1")
                #print((b_x+1, b_y))
                new_board1 = copy_list_by_value(c_game_board)
                new_board1[b_x-ctr][b_y] = " "
                if (b_x+1, b_y) in G[3]:
                    new_board1[b_x+1][b_y] = "#"
                else:
                    new_board1[b_x+1][b_y] = "$"
                if check_dead_state_static(new_board1) == True:
                    pass
                else:
                    return False

                b_x += 1
                ctr += 1

            b_x = b_x - ctr
            ctr = 0


            while (b_x-1, b_y)  in G[1].union(G[3]) and reachable(G[4],(b_x+ ctr + 1, b_y), G) and (b_x+ctr +1, b_y) not in G[2]:
                #print("hi2")
                #print((b_x-1, b_y), "going down")
                #print(b_x, ctr)
                new_board2 = copy_list_by_value(c_game_board)
                new_board2[b_x + ctr][b_y] = " "
                if (b_x-1, b_y) in G[3]:
                    new_board2[b_x-1][b_y] = "#"
                else:
                    new_board2[b_x-1][b_y] = "$"
                if check_dead_state_static(new_board2) == False:
                    return False

                b_x -= 1
                ctr += 1
                #print(b_x, ctr)

            b_x = b_x + ctr
            ctr = 0

            while (b_x, b_y+1)  in G[1].union(G[3]) and reachable(G[4],(b_x, b_y-ctr-1), G) and (b_x, b_y-ctr-1) not in G[2]:
                #print("hi3")
                #print((b_x, b_y+1))
                new_board3 = copy_list_by_value(c_game_board)

                new_board3[b_x][b_y-ctr] = " "
                if (b_x, b_y+1) in G[3]:
                    new_board3[b_x][b_y+1] = "#"
                else:
                    new_board3[b_x][b_y+1] = "$"
                if check_dead_state_static(new_board3) == True:
                    pass
                else:
                    return False
                
                b_y += 1
                ctr += 1

            b_y = b_y - ctr
            ctr = 0
            
            while (b_x, b_y-1)  in G[1].union(G[3]) and reachable(G[4],(b_x, b_y+ ctr +1), G) and (b_x, b_y+ ctr +1) not in G[2]:
                #print("hi4")

                #print((b_x, b_y-1))
                #print("alsfgas")
                #wrapper(c_game_board)
                #print('alsfdgasfdg')
                new_board4 = copy_list_by_value(c_game_board) 
                new_board4[b_x][b_y+ ctr] = " "
                if (b_x, b_y-1) in G[3]:
                    new_board4[b_x][b_y-1] = "#"
                else:
                    new_board4[b_x][b_y-1] = "$"
                #print("asfg")
                #wrapper(new_board4)
                if check_dead_state_static(new_board4) == True:
                    pass
                else:
                    return False

                b_y -= 1
                ctr += 1

            b_y = b_y + ctr
            ctr = 0
        #wrapper(new_board1)
        #print()
        #wrapper(new_board2)
        #print()
        #wrapper(new_board3)
       # print()
        #wrapper(new_board4)

        return True

    else:
        return False



# Not working #1
G1 =  [['#', '#', '#'], ['#', '@', '#'], ['#', '$', '#'], ['#', '.', '#'], ['#', '#', '#']]

# Not working #2
G2 =  [['#', '#', '#', '#', '#', '#', '#', '#'], ['#', '.', ' ', '#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '$', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', '#', ' ', '#', '#'], ['#', '#', ' ', '#', ' ', '$', '.', '#'], ['#', ' ', ' ', ' ', '$', ' ', ' ', '#'], ['#', ' ', ' ', '.', '#', ' ', '@', '#'], ['#', '#', '#', '#', '#', '#', '#', '#']]

# Not working #3
G3 = [['#', '#', '#', '#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#', ' ', '.', '#'], ['#', ' ', '$', ' ', ' ', ' ', '@', '#'], ['#', ' ', '$', '$', '#', '#', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', '.', '#'], ['#', '#', '#', '#', '#', '#', '#', '#']]
 
G4 = [['#', '#', '#', '#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#', ' ', '.', '#'], ['#', '$', ' ', ' ', ' ', ' ', '@', '#'], ['#', '$', ' ', '$', '#', '#', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', '.', '#'], ['#', '#', '#', '#', '#', '#', '#', '#']]
# G1 = [['#', '#', '#', '#', '#', '#', '#', '#'], ['#', '.', '$', '#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', '@', ' ', '$', '#'], ['#', ' ', ' ', ' ', '#', ' ', '#', '#'], ['#', '#', ' ', '#', '$', ' ', '.', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '.', '#', ' ', ' ', '#'], ['#', '#', '#', '#', '#', '#', '#', '#']]
#
# G2 = [['#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#'], ['#', ' ', ' ', '$', '#'], ['#', ' ', ' ', '@', '#'], ['#', '#', '#', '#', '#']]
#
# G3 = [['#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#'], ['#', ' ', ' ', '$', '#'], ['#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '@', '#'], ['#', '#', '#', '#', '#']]
#
# G4 = [['#', '#', '#', '#', '#'], ['#', ' ', ' ', '.', '#'], ['#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '$', '#'], ['#', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '@', '#'], ['#', '#', '#', '#', '#']]
#
def wrapper(G):
    for i in G:
        print(str(i))

#wrapper(G1)
#print(is_dead_state(G1))

#wrapper(G2)
#print(is_dead_state(G2))

#wrapper(G3)
#print(is_dead_state(G3))

#wrapper(G4)
#print(is_dead_state(G4))
#
# print(check_dead_state(G2))
# print(check_dead_state(G3))
# print(check_dead_state(G4))
