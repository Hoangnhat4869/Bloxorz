from solve import Solve
from blockPos import State, Position, Special_Tile
from blockMove import Block
from bNode import BNode
from map import Map

from typing import List, Dict, Tuple

def get_target_position(mat: List[List[int]]) -> Tuple:
        for y in range(len(mat)):
            for x in range(len(mat[0])):
                if mat[y][x] == 9:
                    return x+1, len(mat)-y

def set_spec_tile(mat: List[List[int]]) -> list():
    spec_tile = list()
    for i in range (1, row*col+5):
        spec_tile.append(None)
        
    for y in range (row):
        for x in range (col):
            if 2 < mat[y][x] < 9:
                print("Input the positions that special tile affects to (type:", mat[y][x], ", Pos(",x+1,",", row-y,")): ", end="")
                x1, y1, x2, y2 = map(int, input().split())
                spec_tile[(row-y-1)*col + x+1] = Special_Tile(mat[y][x], x1, y1, x2, y2)

    return spec_tile

                
row = int(input("Enter the number of the map's rows: "))
col = int(input("Enter the number of the map's columns: "))

mat = list()
print("Input map: ")
for y in range (row):
    mat.append(list(map(int, input().split())))

# mat = [
#     [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
#     [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
#     [1, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
#     [0, 0, 0, 0, 0, 1, 9, 1, 0, 0, 2, 2, 1, 2],
#     [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2]
# ]

# mat = [
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
#     [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
# ]

# mat = [
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
# ]

print("Enter the start position: ", end="")
start_x, start_y = map(int, input().split())
while mat[row-start_y][start_x-1] != 1:
    print("Unvalid start position, please choose another position: ", end="")
    start_x, start_y = mat(int, input().split())

#(start_x, start_y) = (2, 4)

spec_tile = set_spec_tile(mat)

blox = Solve(mat, spec_tile)

# Create node
start_pos = Position(start_x, start_y, start_x, start_y, State.STANDING, 1, Map(mat))
block_obj = Block(start_pos)
root_node = BNode(block_obj)

print("Choose an algorithm:\
      1. BFS search\
      2. DFS search\
      3. A* search\
      4. Monte Carlo search")

algorithm = int(input())
if algorithm == 1:
    blox.solve_by_bfs(root_node)
elif algorithm == 2:
    blox.solve_by_dfs(root_node)
elif algorithm == 3:
    x_pos, y_pos = get_target_position(mat)
    print("Choose the distance calculation method for heuristic cost:\
          1. Euclidean\
          2. Manhattan")
    dis = int(input())
    blox.solve_by_astar(root_node, Position(x_pos, y_pos, x_pos, y_pos, State.STANDING, 1, Map(mat)), dis)
elif algorithm == 4:
    blox.solve_by_dfs(root_node)
else:
    print("UNVALID!!!")
    




# mat = dict()
# mat[0] = [
#     [0, 0, 0, 1],
#     [1, 9, 0, 1],
#     [1, 1, 1, 1],
#     [0, 1, 1, 1],
#     [0, 1, 0, 0]
# ]
# mat[1] = [
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
#     [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
# ]
# mat[2] = [
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
# ]

# mat[3] = [
#     [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
#     [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
#     [1, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
#     [0, 0, 0, 0, 0, 1, 9, 1, 0, 0, 2, 2, 1, 2],
#     [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2]
# ]

# 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1
# 0 1 1 1 1 1 1 1 6 1 1 1 1 1 1
# 0 1 1 1 1 0 0 0 0 0 0 0 1 1 1
# 0 1 1 7 1 0 0 0 0 0 0 0 0 0 0
# 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0
# 0 0 0 1 1 1 8 1 1 1 1 1 1 0 0
# 0 0 0 0 0 0 0 0 0 0 1 1 1 1 6
# 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1
# 1 9 1 1 1 1 1 1 1 1 1 1 1 0 0
# 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
# start: 4 9
# 6 9, 7 9
# 6 2, 7 2
# 6 2, 7 2
# 6 2, 7 2


# 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0
# 0 0 0 0 0 1 0 0 1 1 1 0 0 0 0
# 0 0 0 0 0 1 0 0 1 1 1 1 1 0 0
# 1 1 1 1 1 1 0 0 0 0 0 1 1 1 1
# 0 0 0 0 1 1 1 0 0 0 0 1 1 9 1
# 0 0 0 0 1 1 1 0 0 0 0 0 1 1 1
# 0 0 0 0 0 0 1 0 0 1 1 0 0 0 0
# 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0
# 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0
# 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0


# 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0
# 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0
# 1 1 1 0 0 0 0 0 1 0 0 1 1 1 1
# 1 1 1 1 1 1 1 1 1 0 0 0 1 9 1
# 1 1 1 0 0 0 0 1 1 5 0 0 1 1 1
# 1 1 1 0 0 0 0 1 1 1 0 0 1 1 1
# 0 1 1 0 0 0 0 1 0 0 0 0 0 0 0
# 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0
# start: 2 5
# 2 1


# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1
# 1 1 1 1 3 1 0 0 0 1 1 1 1 9 1
# 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1
# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0
# start: 2 5
# 11 8 11 2


# 1 1 1 1 0 0 0 1 0 0 0 1 1 1 1
# 1 1 1 1 0 0 0 1 0 0 0 1 1 3 1
# 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
# 0 0 0 0 0 0 1 9 1 0 0 0 0 0 0
# 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
# start: 2 4
# 13 4 3 4