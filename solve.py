#!/usr/bin/env python3

from typing import List, Dict, Tuple
from math import sqrt, inf
from heapq import heappush, heappop
from collections import namedtuple

from blockPos import State, Position, Special_Tile, Map
from blockMove import Block, Direction
from bNode import BNode

class Solve:

    def __init__(self, map: List[List[int]], spec_tile: list()):
        self.map = map
        self.spec_tile = spec_tile
        self.cost_visited = dict()

    def get_node_depth(self, node: BNode) -> int:
        level = 0
        tmpnode = node
        while tmpnode.parent is not None:
            level += 1
            tmpnode = tmpnode.parent
        return level
    
    def out_of_map(self, pos: Position) -> bool:
        x_max = len(self.map[0])
        y_max = len(self.map)

        if pos.x1 <= 0 or pos.x1 > x_max or pos.x2 <= 0 or pos.x2 > x_max or \
           pos.y1 <= 0 or pos.y1 > y_max or pos.y2 <= 0 or pos.y2 > y_max:
            return True
        
        return False
    
    def standing_on_orange_tile(self, pos: Position) -> bool:
        y_max = len(self.map)

        if pos.state is State.STANDING and pos.maps.maps[y_max-pos.y1][pos.x1-1] == 2:
            return True
        
        return False
    
    def no_tile_pos(self, pos: Position) -> bool:
        y_max = len(self.map)

        if pos.maps.maps[y_max-pos.y1][pos.x1-1] == 0 or pos.maps.maps[y_max-pos.y2][pos.x2-1] == 0:
            return True
        
        return False

    def unvalid_pos(self, pos: Position) -> bool:
        
        if self.out_of_map(pos) or self.standing_on_orange_tile(pos) or self.no_tile_pos(pos):
            return True
        
        return False
    
    def next_valid_move(self, node: BNode, visited_pos: List):
        
        if node.block.pos.state is State.SPLIT:
            for direction in Direction.direcList("LRUDS"):
                # find next position in the given direction
                next_pos = node.block.next_pos(direction, node.block.pos.splblock)

                # invalid, visited or valid ?
                if not self.unvalid_pos(next_pos) and next_pos not in visited_pos:
                    # Update map when blocks on switch tile
                    self.update_map(next_pos, self.spec_tile)
                    yield next_pos, direction

        else:
            for direction in Direction.direcList("LRUD"):
                # find next position in the given direction
                next_pos = node.block.next_pos(direction, node.block.pos.splblock)

                # invalid, visited or valid ?
                if not self.unvalid_pos(next_pos) and next_pos not in visited_pos:
                    
                    # Update map when blocks on switch tile
                    self.update_map(next_pos, self.spec_tile)
                    yield next_pos, direction
 
    def is_goal(self, pos: Position) -> bool:

        if pos.state is State.STANDING and pos.maps.maps[len(self.map)-pos.y1][pos.x1-1] == 9:
            return True
        return False
    
    def show(self, block: Block):

        style = dict({
            "block": "🟥",
            "hole": "⬛",
            "tile": "⬜",
            "orange_tile": "🟧",
            "split": "🔄 ",
            "X_shaped": "❎",
            "O_shaped": "⏺ ",
            "goal": "🏁"
        })
        
        for y in range(len(block.pos.maps.maps)):
            for x in range(len(block.pos.maps.maps[0])):
                if [x, y] in [[block.pos.x1-1, len(block.pos.maps.maps)-block.pos.y1], [block.pos.x2-1, len(block.pos.maps.maps)-block.pos.y2]]:
                    print(style['block'], end="")
                elif block.pos.maps.maps[y][x] == 0:
                    print(style['hole'], end="")
                elif block.pos.maps.maps[y][x] == 1:
                    print(style['tile'], end="")
                elif block.pos.maps.maps[y][x] == 2:
                    print(style['orange_tile'], end="")
                elif block.pos.maps.maps[y][x] == 3:
                    print(style['split'], end="")
                elif block.pos.maps.maps[y][x] == 4 or block.pos.maps.maps[y][x] == 5:
                    print(style['X_shaped'], end="")
                elif block.pos.maps.maps[y][x] == 6 or block.pos.maps.maps[y][x] == 7 or block.pos.maps.maps[y][x] == 8:
                    print(style['O_shaped'], end="")
                else:
                    print(style['goal'], end="")

            print("")
        print("")

    def show_optimal_path(self, node: BNode):

        node_stack = list()
        while node is not None:
            node_stack.append(node)
            node = node.parent

        # pop and print the list items
        while len(node_stack) > 0:
            node = node_stack.pop()
            if node.dir_from_parent is None:
                print("[START] ", end="")
                #self.show(node.block)
            else:
                print("-> {} ".format(node.dir_from_parent.name.lower()), end="")
                #self.show(node.block)
        print("[GOAL]")

    def solve_by_bfs(self, head: BNode):

        # visited list to store visited position on the world map.
        visited_pos = list()
        visited_pos.append(head.block.pos)

        # queue to hold nodes encountered at each level of the tree.
        node_queue = list()
        node_queue.append(head)
        while len(node_queue) > 0:
            node = node_queue.pop(0)

            if self.is_goal(node.block.pos):
                print("\nBFS SEARCH COMPLETED ^^")
                print("Steps:", self.get_node_depth(node))
                print("Optimal path: ")
                self.show_optimal_path(node)
                return

            for next_pos, direction in self.next_valid_move(node, visited_pos):

                # #print("pos: ", str(node.block.pos.maps.maps))
                # print("bef: ", str(node.block.pos.maps.maps))
                # Update map when blocks on switch tile
                #self.update_map(next_pos, self.spec_tile)
                # next_pos = Position(1,1,2,2,State.STANDING,1,Map(self.map))
                # print("par: ", str(node.block.pos.maps.maps))
                # create a new block with next_pos, initialize a new node with block position
                new_block = Block(next_pos)
                new_node = BNode(new_block)

                

                # set the 4 direction attributes
                setattr(node, direction.name.lower(), new_node)

                #new_node.block.pos.maps.maps = node.block.pos.maps.maps

                # and parent node of the new node.
                new_node.parent = node
                new_node.dir_from_parent = direction

                #print("new: ", str(new_node.block.pos.maps))
                #self.show(new_node.block)
                node_queue.append(new_node)
                visited_pos.append(next_pos)
        return
    
    def solve_by_dfs(self, node: BNode, visited_pos: List = None):

        if visited_pos is None:
            visited_pos = list()
            visited_pos.append(node.block.pos)

        if self.is_goal(node.block.pos):
            print("\nDFS SEARCH COMPLETED ^^")
            print("Steps:", self.get_node_depth(node))
            print("Optimal path: ")
            self.show_optimal_path(node)
            exit(0)

        for next_pos, direction in self.next_valid_move(node, visited_pos):

            # Update map when blocks on switch tile
            #self.update_map(next_pos, self.spec_tile)

            # create a new block with next_pos, initialize a new node with block position
            # and recursively make the state tree.
            new_block = Block(next_pos)
            new_node = BNode(new_block)

            # self.show(new_block)

            # set the 4 direction attributes
            setattr(node, direction.name.lower(), new_node)

            # and parent node of the new node.
            new_node.parent = node
            new_node.dir_from_parent = direction
            visited_pos.append(next_pos)

            self.solve_by_dfs(new_node, visited_pos)
        return

    def distance_euclidean(self, pos1: Position, pos2: Position) -> float:
        return min(sqrt((pos1.x1 - pos2.x1) ** 2 + (pos1.y1 - pos2.y1) ** 2), sqrt((pos1.x2 - pos2.x2) ** 2 + (pos1.y2 - pos2.y2) ** 2))

    def distance_manhattan(self, pos1: Position, pos2: Position) -> int:
        return min(abs(pos1.x1 - pos2.x1) + abs(pos1.y1 - pos2.y1), abs(pos1.x2 - pos2.x2) + abs(pos1.y2 - pos2.y2))

    def compute_heuristic_costs(self, target_pos: Position, choose: int) -> Dict:

        costs = dict()
        num = 1
        y_max = len(self.map)
        x_max = len(self.map[0])
        for y in range(y_max):
            for x in range(x_max):
                pos = Position(x+1, y_max-y, x+1, y_max-y, State.STANDING, 1, target_pos.maps)
                if not self.no_tile_pos(pos):
                    if choose == 1:
                        costs[num] = self.distance_euclidean(pos, target_pos)
                    else:
                        costs[num] = self.distance_manhattan(pos, target_pos)
                else:
                    costs[num] = inf
                num += 1
        return costs

    def min_h_cost(self, h_costs: dict, node: BNode):

        pos = node.block.pos
        
        x_max = len(self.map[0])
        y_max = len(self.map)

        return min(h_costs[(y_max-pos.y1)*x_max + pos.x1], h_costs[(y_max-pos.y2)*x_max + pos.x2])

    def get_cost_visited(self, pos: Position) -> int:
        
        cost = namedtuple("cost", ['x1', 'y1', 'x2', 'y2', 'state', 'splblock', 'maps'])
        index = cost(x1=pos.x1, y1=pos.y1, x2=pos.x2, y2=pos.y2, state=pos.state, splblock=pos.splblock, maps=pos.maps)
        return self.cost_visited[index]

    def set_cost_visited(self, pos: Position, value: int):

        cost = namedtuple("cost", ['x1', 'y1', 'x2', 'y2', 'state', 'splblock', 'maps'])
        index = cost(x1=pos.x1, y1=pos.y1, x2=pos.x2, y2=pos.y2, state=pos.state, splblock=pos.splblock, maps=pos.maps)
        self.cost_visited[index] = value

    def solve_by_astar(self, head: BNode, target_pos: Position, choose: int):

        # compute the heuristic cost from all valid positions to the target positions
        heuristic_costs = self.compute_heuristic_costs(target_pos, choose)
        head.f_cost = self.min_h_cost(heuristic_costs, head)
        self.set_cost_visited(head.block.pos, 0)

        expanded_nodes = list()
        steps = 0
        
        node = head

        while True:
            for next_pos, direction in self.next_valid_move(node, []):

                g_cost = self.get_cost_visited(node.block.pos) + 1

                # if the node is not visited, add to expanded queue.
                # if the node is visited, but has lower actual cost than previously recorded, add to expanded queue.
                if next_pos not in self.cost_visited or g_cost < self.get_cost_visited(next_pos):
                    
                    # Update map when blocks on switch tile
                    # self.update_map(next_pos, self.spec_tile)
                    
                    # new node and estimated cost.
                    new_node = BNode(Block(next_pos))
                    
                    h_cost = self.min_h_cost(heuristic_costs, new_node)

                    new_node.f_cost = g_cost + h_cost
                    target_pos.maps.maps = next_pos.maps.maps

                    # set current node's child pointer.
                    setattr(node, direction.name.lower(), new_node)

                    # link new_node to the current node.
                    new_node.parent = node
                    new_node.dir_from_parent = direction
                    heappush(expanded_nodes, new_node)

            node = heappop(expanded_nodes)

            # update cost of this node
            self.set_cost_visited(node.block.pos, self.get_cost_visited(node.parent.block.pos) + 1)

            

            # if goal state is dequeued, mark the search as completed.
            if self.is_goal(node.block.pos):
                break

        print("\nA* SEARCH COMPLETED ^^")
        print("Steps:", self.get_node_depth(node))
        print("Optimal path: ")
        self.show_optimal_path(node)
        return

    def update_map(self, pos: Position, spec_tile: list()) -> Position:

        #print((pos.y1-1)*len(self.map[0]) + pos.x1)
        sp = spec_tile[(pos.y1-1)*len(self.map[0]) + pos.x1]
        if pos.state is State.STANDING:
            if sp is None:
                return
            
            if sp.type == 3:
                pos.state = State.SPLIT
                pos.x1 = sp.x1
                pos.y1 = sp.y1
                pos.x2 = sp.x2
                pos.y2 = sp.y2
                pos.block = 1
            elif sp.type == 4 or sp.type == 6:
                pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1 - pos.maps.maps[len(self.map)-sp.y1][sp.x1-1]
                pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1 - pos.maps.maps[len(self.map)-sp.y2][sp.x2-1]
            elif sp.type == 5 or sp.type == 7:
                pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1
                pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1
            elif sp.type == 8:
                pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 0
                pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 0

        else:
            if sp is None:
                sp = spec_tile[(pos.y2-1)*len(self.map[0]) + pos.x2]
                if sp is None:
                    return
                
                if sp.type == 6:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1 - pos.maps.maps[len(self.map)-sp.y1][sp.x1-1]
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1 - pos.maps.maps[len(self.map)-sp.y2][sp.x2-1]
                elif sp.type == 7:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1
                elif sp.type == 8:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 0
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 0
            else:
                if sp.type == 6:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1 - pos.maps.maps[len(self.map)-sp.y1][sp.x1-1]
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1 - pos.maps.maps[len(self.map)-sp.y2][sp.x2-1]
                elif sp.type == 7:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 1
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 1
                elif sp.type == 8:
                    pos.maps.maps[len(self.map)-sp.y1][sp.x1-1] = 0
                    pos.maps.maps[len(self.map)-sp.y2][sp.x2-1] = 0

