from __future__ import annotations
from typing import List
from enum import Enum
from blockPos import Position, State


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def direcList(dStr: str) -> List[Direction]:
        """
        Return list of direction enumeration
        """
        char_map = {
            'U': Direction.UP,
            'D': Direction.DOWN,
            'L': Direction.LEFT,
            'R': Direction.RIGHT
        }
        dirList = list()
        for char in dStr:
            dirList.append(char_map[char])

        return dirList
    

class Block:

    def __init__(self, pos: Position):
        self.pos = pos


    def next_pos(self, dir: Direction, block: int) -> Position:

        nextpos = Position(self.pos.x1, self.pos.y1, self.pos.x2, self.pos.y2, self.pos.state)

        if self.pos.state is State.STANDING:
            if dir is Direction.UP:
                nextpos.y1 += 2
                nextpos.y2 += 1
                nextpos.state = State.VERTICAL
            if dir is Direction.DOWN:
                nextpos.y1 -= 1
                nextpos.y2 -= 2
                nextpos.state = State.VERTICAL
            if dir is Direction.LEFT:
                nextpos.x1 -= 2
                nextpos.x2 -= 1
                nextpos.state = State.HORIZONTAL
            if dir is Direction.RIGHT:
                nextpos.x1 += 1
                nextpos.x2 += 2
                nextpos.state = State.HORIZONTAL
            nextpos.update_pos()

        elif self.pos.state is State.VERTICAL:
            if dir is Direction.UP:
                nextpos.y1 += 1
                nextpos.y2 += 2
                nextpos.state = State.STANDING
            if dir is Direction.DOWN:
                nextpos.y1 -= 2
                nextpos.y2 -= 1
                nextpos.state = State.STANDING
            if dir is Direction.LEFT:
                nextpos.x1 -= 1
                nextpos.x2 -= 1
            if dir is Direction.RIGHT:
                nextpos.x1 += 1
                nextpos.x2 += 1
            nextpos.update_pos()


        elif self.pos.state is State.HORIZONTAL:
            if dir is Direction.UP:
                nextpos.y1 += 1
                nextpos.y2 += 1
            if dir is Direction.DOWN:
                nextpos.y1 -= 1
                nextpos.y2 -= 1
            if dir is Direction.LEFT:
                nextpos.x1 -= 1
                nextpos.x2 -= 2
                nextpos.state = State.STANDING
            if dir is Direction.RIGHT:
                nextpos.x1 += 2
                nextpos.x2 += 1
                nextpos.state = State.STANDING
            nextpos.update_pos()


        elif self.pos.state is State.SPLIT:
            if block == 1:
                if dir is Direction.UP:
                    nextpos.y1 += 1
                if dir is Direction.DOWN:
                    nextpos.y1 -= 1
                if dir is Direction.LEFT:
                    nextpos.x1 -= 1
                if dir is Direction.RIGHT:
                    nextpos.x1 += 1
            if block == 2:
                if dir is Direction.UP:
                    nextpos.y1 += 1
                if dir is Direction.DOWN:
                    nextpos.y1 -= 1
                if dir is Direction.LEFT:
                    nextpos.x1 -= 1
                if dir is Direction.RIGHT:
                    nextpos.x1 += 1

            ### Update position when 2 blocks collided

            if abs(nextpos.x1 - nextpos.x2) == 1 and nextpos.y1 == nextpos.y2:
                nextpos.state = State.HORIZONTAL
                nextpos.update_pos()

            elif abs(nextpos.y1 - nextpos.y2) == 1 and nextpos.x1 == nextpos.x2:
                nextpos.state = State.VERTICAL
                nextpos.update_pos()

        return nextpos
    
    def move(self, next_pos: Position):
        """
        Move the brick to the given position.
        :param next_pos: Position object.
        """
        self.pos = next_pos