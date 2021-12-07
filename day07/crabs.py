import math
import timeit
import matplotlib.pyplot as plt

test = """16,1,2,0,4,2,7,1,2,14"""

def parse_input(contents):
    return list(map(int, contents.split(',')))

# O(C*R)
def min_pos(crabs, cost_fn= lambda x,y: abs(x - y)):
    num_spots = max(crabs) - min(crabs)

    best = float('inf')
    for hpos in range(min(crabs), max(crabs) + 1):
        cost = 0
        for crab in crabs:
            cost += cost_fn(crab, hpos)

        best = min(best, cost)

    return best

# O(C * lg(R))
def min_pos_l1(crabs, cost_fn= lambda x,y: abs(x - y)):

    memo = {}
    def tc(pos): # total cost
        if pos not in memo:
            cost = 0
            for crab in crabs:
                cost += cost_fn(crab, pos)
            memo[pos] = cost
        return memo[pos]

    def slope(pos):
        left, center, right = pos - 1, pos, pos + 1
        if tc(center) <= tc(left) and tc(center) <= tc(right):
            return 0 # critical point 
        elif tc(left) <= tc(center) <= tc(center):
            return 1
        elif tc(left) >= tc(center) >= tc(center):
            return -1

    lo, hi = min(crabs), max(crabs)
    while lo < hi - 1:
        mid = (lo + hi) // 2

        ls, ms, hs = slope(lo), slope(mid), slope(hi)

        if ls == 0 or ms == 0 or hs == 0: # if one of these is the 
            return min(tc(lo), tc(mid), tc(hi))
        elif (ls, ms, hs) == (-1, -1, 1):
            lo = mid
        elif (ls, ms, hs) == (-1, 1, 1):
            hi = mid
        else:
            print((ls, ms, hs))

    return min(tc(lo), tc(hi))

# O (C)
def min_pos_l2(crabs):
    def cost_fn(a, b):
        dist = abs(a - b)
        return (dist * (dist + 1)) / 2

    def total_cost(pos):
        cost = 0
        for crab in crabs:
            cost += cost_fn(crab, pos)

        return cost

    pos = sum(crabs) / len(crabs)
    return int( # answer is on of the ints beside the mean
                min(
                    total_cost(math.floor(pos)),
                    total_cost(math.ceil(pos))
                )
            )

        

if __name__ == "__main__":
    crabs = parse_input(test)

    print(min_pos_l1(crabs))

    print('--- Part 1 ---')
    with open('day07/input.txt') as f:
        crabs = parse_input(f.read())

    # print(timeit.timeit(lambda: min_pos(crabs), number=10))
    # print(timeit.timeit(lambda: min_pos_l1(crabs), number=10))
    print(min_pos_l1(crabs))    

    print('--- Part 2 ---')

    print(min_pos_l2(crabs))