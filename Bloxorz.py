# #!/usr/bin/env python3

# from typing import List, Dict, Tuple
# from math import sqrt, inf
# import argparse
# from heapq import heappush, heappop
# from collections import namedtuple

# from blockPos import State, Position
# from blockMove import Block, Direction
# from bNode import BNode

# class Bloxorz:

#     def __init__(self, map: List[List[int]]):
#         self.map = map
#         self.dfs_steps = 0


#     def get_node_depth(self, node: BNode) -> int:
#         """
#         Compute the depth of a given tree node.
#         :param node: Tree node.
#         :return: Depth value as distance of the node from the root node.
#         """
#         level = 0
#         tmpnode = node
#         while tmpnode.parent is not None:
#             level += 1
#             tmpnode = tmpnode.parent
#         return level


#     def unvalid_pos(self, pos: Position) -> bool:
        
#         x_max = len(self.map[0])
#         y_max = len(self.map)


#         ### Out of map:
#         if pos.x1 <= 0 or pos.x1 > x_max or pos.x2 <= 0 or pos.x2 > x_max or \
#            pos.y1 <= 0 or pos.y1 > y_max or pos.y2 <= 0 or pos.y2 > y_max:
#             return True

#         #print(pos.x1-1, y_max-pos.y1, pos.x2-1, y_max-pos.y2, self.map[y_max-pos.y1][pos.x1-1], self.map[y_max-pos.y2][pos.x2-1])
#         ### Standing on orange tile:
#         if pos.state is State.STANDING and self.map[y_max-pos.y1][pos.x1-1] == 2:
#             return True
        
#         ### no-tile positions:
#         if self.map[y_max-pos.y1][pos.x1-1] == 0 or self.map[y_max-pos.y2][pos.x2-1] == 0:
#             #print("out")
#             return True
        
#         return False
    

#     def next_valid_move(self, node: BNode, visited_pos: List):

#         for direction in Direction.direcList("LRUD"):
#             # find next position in the given direction
#             next_pos = node.block.next_pos(direction, 1)

#             # invalid, visited or valid ?
#             if not self.unvalid_pos(next_pos) and next_pos not in visited_pos:
#                 #print(str(next_pos), str(direction))
#                 yield next_pos, direction

    
#     def is_goal(self, pos: Position) -> bool:

#         if pos.state is State.STANDING and self.map[len(self.map)-pos.y1][pos.x1-1] == 9:
#             return True
#         return False
    

#     def show(self, brick: Block):

#         style = dict({
#             "tile": "⬜",
#             "hole": "⬛",
#             "brick": "🟧",
#             "target": "❎"
#         })

#         for y in range(len(self.map)):
#             for x in range(len(self.map[0])):
#                 if [x, y] in [[brick.pos.x1-1, len(self.map)-brick.pos.y1], [brick.pos.x2-1, len(self.map)-brick.pos.y2]]:
#                     print(style['brick'], end="")
#                 elif self.map[y][x] == 9:
#                     print(style['target'], end="")
#                 else:
#                     tile_char = style['tile'] if self.map[y][x] == 1 else style['hole']
#                     print(tile_char, end="")

#             print("")
#         print("")


#     def show_optimal_path(self, node: BNode):

#         node_stack = list()
#         while node is not None:
#             node_stack.append(node)
#             node = node.parent

#         # pop and print the list items
#         while len(node_stack) > 0:
#             node = node_stack.pop()
#             if node.dir_from_parent is None:
#                 print("[START] ")
#                 self.show(node.block)
#             else:
#                 # print("-> {} ".format(node.dir_from_parent.name.lower()), end="")
#                 self.show(node.block)
#         print("[GOAL]\n\n")

    
#     def solve_by_bfs(self, head: BNode):

#         # visited list to store visited position on the world map.
#         visited_pos = list()
#         visited_pos.append(head.block.pos)

#         # queue to hold nodes encountered at each level of the tree.
#         node_queue = list()
#         node_queue.append(head)

#         steps = 0
#         while len(node_queue) > 0:
#             node = node_queue.pop(0)

#             # show the BFS tree.
#             # print("Step: {}, Depth: {}, - {}".format(steps, self.get_node_depth(node), str(node)))
#             # self.show(node.block)

#             steps += 1
#             if self.is_goal(node.block.pos):
#                 print("\nBFS SEARCH COMPLETED !")
#                 print("Optimal path is as below -> \n")
#                 self.show_optimal_path(node)
#                 return

#             for next_pos, direction in self.next_valid_move(node, visited_pos):
#                 # create a new brick with next_pos, initialize a new node with brick position
#                 new_brick = Block(next_pos)
#                 new_node = BNode(new_brick)

#                 # set the 4 direction attributes
#                 setattr(node, direction.name.lower(), new_node)

#                 # and parent node of the new node.
#                 new_node.parent = node
#                 new_node.dir_from_parent = direction

#                 node_queue.append(new_node)
#                 visited_pos.append(next_pos)
#         return


# # if __name__ == '__main__':

# matrix = [
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
#     [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
# ]

# # matrix = [
# #     [0, 0, 0, 1],
# #     [1, 9, 0, 1],
# #     [1, 1, 1, 1],
# #     [0, 1, 1, 1],
# #     [0, 1, 0, 0]
# # ]

# blox = Bloxorz(matrix)

# (start_x, start_y) = (2, 3)

# # initialize the brick to (0 based index) x,y coordinates and a standing orientation.
# start_pos = Position(start_x, start_y, start_x, start_y, State.STANDING)
# brick_obj = Block(start_pos)
# root_node = BNode(brick_obj)

# blox.solve_by_bfs(root_node)