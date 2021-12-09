from pprint import pprint
from tqdm import trange

test = """2199943210
3987894921
9856789892
8767896789
9899965678"""

def parse_input(contents):
    return [list(map(int, row)) for row in contents.split('\n')]

def neighbors(cave, y, x):
    for dx, dy in [(1,0), (0, 1), (-1, 0), (0, -1)]:
        if 0 <= dx + x < len(cave[0]) and 0 <= dy + y < len(cave):
            yield (y + dy, x + dx)

def is_low(cave, y, x):
    for ny, nx in neighbors(cave, y, x):
        if cave[y][x] >= cave[ny][nx]:
            return False
            
    return True

def assess_risk(cave):
    risk = 0
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if is_low(cave, y, x):
                risk += cave[y][x] + 1

    return risk

def size_of_basin(cave, y, x):
    frontier = [(y, x)]
    visited = set()
    while frontier:
        pos = frontier.pop()
        y, x = pos
        
        if pos in visited:
            continue
        visited.add(pos)

        for ny, nx in neighbors(cave, y, x):
            if cave[ny][nx] >= cave[y][x] and cave[ny][nx] != 9:
                frontier.append((ny, nx))
    
    return len(visited)

def top_basins(cave):
    sizes = []
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if is_low(cave, y, x):
                sizes.append(size_of_basin(cave, y, x))

    sizes.sort()

    return sizes[-3] * sizes[-2] * sizes[-1]

if __name__ == "__main__":
    cave = parse_input(test)

    print(assess_risk(cave))
    print(top_basins(cave))


    print('---- Part 1 ----')
    with open('day09/input.txt') as f:
        cave = parse_input(f.read())
    
    print(assess_risk(cave))
    
    print('---- Part 2 ----')
    print(top_basins(cave))