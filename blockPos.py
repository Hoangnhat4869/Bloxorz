from __future__ import annotations
from enum import Enum
from map import Map
from typing import List

class State(Enum):
    STANDING = 1
    VERTICAL = 2
    HORIZONTAL = 3
    SPLIT = 4


class Position:

    def __init__(self, x1: int, y1: int, x2: int, y2: int, 
                 state: State = State.STANDING, splblock = 1, maps = Map()):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.state = state
        self.splblock = splblock
        self.maps = maps

    def update_pos(self):

        if (self.x1>self.x2 or self.y1<self.y2):
            self.x1, self.x2 = self.x2, self.x1
            self.y1, self.y2 = self.y2, self.y1
            
    def __hash__(self):
        return hash((self.x1, self.y1, self.x2, self.y2 ,self.state, self.splblock, self.maps))

    def __str__(self):
        return '[x1:{}, y1:{}, x2:{}, y2:{}, state:{}, splblock:{}, maps:{}]'.format(self.x1, self.y1, self.x2, self.y2 ,self.state, self.splblock, self.maps)

    def __eq__(self, other: Position) -> bool:
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2 and self.state == other.state and self.splblock == other.splblock and self.maps == other.maps
    

class Special_Tile:

    def __init__(self, type: int, aff: list()):
        self.type = type
        self.aff = aff
