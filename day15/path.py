from copy import deepcopy
from os import fpathconf
from pprint import pprint
import heapq as hq

def parse_input(contents):
    return [list(map(int, row)) for row in contents.split('\n')]

class TiledMap:
    def __init__(self, map, factor=1) -> None:
        self._base_map = deepcopy(map)
        self.factor = factor

    def __getitem__(self, index):
        H, W = len(self._base_map), len(self._base_map[0])
        y, x = index

        cost = (self._base_map[y % H][x % W] + (y // H) + (x // W) - 1) % 9
        return cost + 1

    def get_dimensions(self):
        return len(self._base_map) * self.factor, len(self._base_map[0]) * self.factor

# A* search
def minpath(cave_map: TiledMap):
    H, W = cave_map.get_dimensions()
    def neighbors(y, x):
        for dx, dy in [(1,0), (0, 1), (-1, 0), (0, -1)]:
            if 0 <= dx + x < W and 0 <= dy + y < W:
                yield (y + dy, x + dx)
        
    def h(y, x):
        return (H - 1 - y + W - 1 - x)
    
    # h(x) + running_cost, running_cost, x
    frontier = [(h(0,0), 0, (0,0))]
    visited = set()
    while frontier:
        _, cost, pos = hq.heappop(frontier)
        y, x = pos

        if pos in visited:
            continue
        visited.add(pos)

        if (y, x) == (H - 1, W - 1):
            return cost

        for ny, nx in neighbors(y, x):
            ncost = cost + cave_map[ny, nx]
            hq.heappush(frontier, (ncost + h(ny, nx), ncost, (ny, nx)))



if __name__ == "__main__":
    with open('day15/test.txt') as f:
        cave_map = parse_input(f.read()) 
    small_map = TiledMap(cave_map)
    big_map = TiledMap(cave_map, factor=5)
    print(minpath(small_map))
    print(minpath(big_map))

    print('--- Part 1 ---')
    with open('day15/input.txt') as f:
        cave_map = parse_input(f.read())

    small_map = TiledMap(cave_map)
    print(minpath(small_map))

    print('--- Part 2 ---')
    big_map = TiledMap(cave_map, factor=5)
    print(minpath(big_map))