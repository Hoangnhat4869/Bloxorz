from __future__ import annotations
from typing import List

class Map:
    def __init__(self, maps: List[List[int]] = list()):
        self.maps = list()
        for i in range(len(maps)):
            temp = list()
            for j in range(len(maps[0])):
                temp.append(maps[i][j])
            self.maps.append(temp)

    def __eq__(self, other: Map) -> bool:
        return self.maps == other.maps
    
    def __hash__(self):
        return hash(str(self.maps))