from itertools import count, product
from copy import deepcopy
from pprint import pprint

def neighbors(arr, y, x):
    for dx, dy in product([-1, 0, 1], repeat=2):
        if (dx, dy) == (0, 0): continue # Not a neighbor of yourself

        # Yield in-bounds neighobrs
        if 0 <= dx + x < len(arr[0]) and 0 <= dy + y < len(arr):
            yield (y + dy, x + dx)

def step(octs):
    # Initial cells we need to visit (all of them)
    frontier = [(i,j) for i in range(len(octs)) for j in range(len(octs[0]))]
    while frontier:
        i, j = frontier.pop()

        # Increment self
        octs[i][j] += 1

        # Only flash when first excited
        if octs[i][j] != 10: continue

        # Add neighbors to increment
        for ni, nj in neighbors(octs, i, j):
            frontier.append((ni, nj))
    
    # Set flashes back to 0
    count = 0
    for i in range(len(octs)):
        for j in range(len(octs[0])):
            if octs[i][j] > 9:
                octs[i][j] = 0
                count += 1

    return count

def count_flashes(octs, steps):
    total = 0
    for _ in range(steps):
        total += step(octs)

    return total

def find_sync(octs):
    s = 1
    while not step(octs) == len(octs) * len(octs[0]):
        s += 1
    return s

def parse_input(contents):
    return [list(map(int, line)) for line in contents.splitlines()]

if __name__ == "__main__":
    with open('day11/test.txt') as f:
        test = parse_input(f.read())

    print(count_flashes(deepcopy(test), 100))
    print(find_sync(deepcopy(test)))

    print('--- Part 1 ---')
    with open('day11/input.txt') as f:
        octs = parse_input(f.read())

    print(count_flashes(deepcopy(octs), 100))

    print('--- Part 2 ---')
    print(find_sync(deepcopy(octs)))