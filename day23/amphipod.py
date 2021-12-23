import heapq as hq
from pprint import pprint
import tqdm

COSTS = {'A':1, 'B':10, 'C': 100, 'D': 1000}
TARGETS = {'A': 3, 'B': 5, 'C':7, 'D':9}

def has_path(state, start, end, ignore_pods=False):
    frontier = [(start, 0, 0)]
    counted = set()
    visited = set()
    while frontier:
        pos, depth, aux = frontier.pop()
        y, x = pos

        if pos == end:
            return True, depth, aux

        if pos in visited: continue
        visited.add(pos)

        for dy, dx in [(1,0),(0,1),(-1,0),(0,-1)]:
            if not (0 <= y + dy < len(state)) or not (0 <= x + dx < len(state[0])):
                continue

            if not ignore_pods and state[y + dy][x + dx] != '.':
                continue
            elif ignore_pods and state[y + dy][x + dx] not in '.ABCD':
                continue

            if state[y + dy][x + dx] in 'ABCD' and (y + dy, x + dx) != start and (y + dy, x + dx) not in counted:
                aux += COSTS[state[y + dy][x + dx]] 
                counted.add((y + dy, x + dx))

            frontier.append(((y + dy, x + dx), depth + 1, aux))

    return False, None, None

def greedy_placement(state):
    for y in range(len(state)):
        for x in range(len(state[0])):
            cell = state[y][x]
            if cell == '.' or cell == '#': continue

def done(state):
    size = len(state) - 3
    return (
        'A'*size == ''.join(state[i][3] for i in range(2, len(state)-1)) and
        'B'*size == ''.join(state[i][5] for i in range(2, len(state)-1)) and
        'C'*size == ''.join(state[i][7] for i in range(2, len(state)-1)) and
        'D'*size == ''.join(state[i][9] for i in range(2, len(state)-1))
    )

def is_in_place(state, pos):
    y, x = pos
    if state[y][x] in '.#': return False
    if x != TARGETS[state[y][x]]: return False

    for iy in range(y + 1, len(state)):
        if state[iy][x] != state[y][x] and state[iy][x] != '#':
            return False
    
    return True

def neighbors(state):
    for y in range(len(state)):
        for x in range(len(state[0])):
            cell = state[y][x]
            if cell == '.' or cell == '#': continue
            if is_in_place(state, (y, x)): continue

            # get the desired position for this one
            ty = len(state) - 2
            while state[ty][TARGETS[cell]] == cell:
                ty -= 1

            exists, steps, _ = has_path(state, (y,x), (ty, TARGETS[cell]))
            if exists:
                newstate = list(map(list, state))
                newstate[ty][TARGETS[cell]] = newstate[y][x]
                newstate[y][x] = '.'

                yield tuple(map(tuple, newstate)), COSTS[cell] * steps
                return

    for y in range(len(state)):
        for x in range(len(state[0])):
            cell = state[y][x]
            if cell == '.' or cell == '#': continue
            if is_in_place(state, (y, x)): continue


            for dy, dx in [(1,0),(0,1),(-1,0),(0,-1)]:
                if not (0 <= y + dy < len(state)) or not (0 <= x + dx < len(state[0])) or state[y + dy][x + dx] != '.':
                    continue
                newstate = list(map(list, state))
                newstate[y + dy][x + dx] = newstate[y][x]
                newstate[y][x] = '.'

                yield tuple(map(tuple, newstate)), COSTS[cell]


def h(state):
    total = 0
    for y in range(len(state)):
        for x in range(len(state[0])):
            cell = state[y][x]
            if cell == '.' or cell == '#': continue
            if is_in_place(state, (y, x)): continue
            # if cell != 'D': continue

            # ty = len(state) - 2
            # while state[ty][TARGETS[cell]] == cell:
            #     ty -= 1

            _, depth, aux = has_path(state, (y,x), (2, TARGETS[cell]), True)

            total += depth * COSTS[cell]# + aux
    return total

def print_state(state):
    print('\n'.join(''.join(line) for line in state))

def min_path(start):
    
    # (cum + h, cum, state)
    frontier = [(0 + h(start), 0, start)]
    visited = set()
    pbar = tqdm.tqdm()
    while frontier:
        estimated_cost, cumulative_cost, state = hq.heappop(frontier)
        pbar.update()
        pbar.set_description(f"{estimated_cost}:{cumulative_cost}")
        if pbar.n % 10**3 == 0:
            print_state(state)
        # print('---')  
        # print(cumulative_cost)
        # print_state(state)

        if done(state):
            return cumulative_cost

        if state in visited: continue
        visited.add(state)

        for neighbor, cost in neighbors(state):
            total_cost = cumulative_cost + cost
            hq.heappush(frontier, (total_cost + h(neighbor), total_cost, neighbor))

    return -1

if __name__ == "__main__":
# test heuristic
#     start = """#############
# #......D.C..#
# ###A#B#.#.###
# ###A#B#C#D###
# #############"""
# test
#     start = """#############
# #...........#
# ###B#C#B#D###
# ###A#D#C#A###
# #############"""
# test 2
#     start = """#############
# #...........#
# ###B#C#B#D###
# ###D#C#B#A###
# ###D#B#A#C###
# ###A#D#C#A###
# #############"""
# Part 1
#     start = """#############
# #...........#
# ###D#B#A#C###
# ###B#D#A#C###
# #############"""
# Part 2
    start = """#############
#...........#
###D#B#A#C###
###D#C#B#A###
###D#B#A#C###
###B#D#A#C###
#############"""

    start = tuple(map(tuple, start.splitlines()))

    print(min_path(start))
    # print(h(start))
    # for y in range(len(start)):
    #     for x in range(len(start[0])):
    #         print(is_in_place(start, (y, x)), end='')
    #     print()