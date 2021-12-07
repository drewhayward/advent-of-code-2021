test = """16,1,2,0,4,2,7,1,2,14"""

def parse_input(contents):
    return list(map(int, contents.split(',')))

def min_pos(crabs, cost_fn= lambda x,y: abs(x - y)):
    num_spots = max(crabs) - min(crabs)

    best = float('inf')
    for hpos in range(min(crabs), max(crabs) + 1):
        cost = 0
        for crab in crabs:
            cost += cost_fn(crab, hpos)

        best = min(best, cost)

    return best
        

if __name__ == "__main__":
    crabs = parse_input(test)

    print(min_pos(crabs))

    print('--- Part 1 ---')
    with open('day07/input.txt') as f:
        crabs = parse_input(f.read())

    print(min_pos(crabs))    

    print('--- Part 2 ---')
    
    def cost2(a, b):
        dist = abs(a - b)
        return (dist * (dist + 1)) / 2

    print(min_pos(crabs, cost2))