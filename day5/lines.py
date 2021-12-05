from typing import DefaultDict
from collections import defaultdict

# test = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2"""

test = """0,9 -> 5,9
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
0,9 -> 2,9
3,4 -> 1,4"""

# test = """0,9 -> 5,9
# 0,9 -> 2,9"""

def get_dir(line):
    x1, y1, x2, y2 = line

    dx = None
    if x1 == x2:
        dx = 0
    elif x1 > x2:
        dx = -1
    else:
        dx = 1
    
    dy = None
    if y1 == y2:
        dy = 0
    elif y1 > y2:
        dy = -1
    else:
        dy = 1

    return (dx, dy)

def count_danger(lines, diag=False):
    counts = defaultdict(int)
    for line in lines:
        x1, y1, x2, y2 = line
        direction = get_dir(line)
        if not diag and 0 not in direction: # Consider only horz/vert
            continue
        curr = (x1, y1)
        end = (x2, y2)
        if curr == end:
            counts[curr] += 1
            continue
        while curr != end:
            counts[curr] += 1
            curr = curr[0] + direction[0], curr[1] + direction[1]
        counts[end] += 1

        
    return sum((1 for v in counts.values() if v >= 2))

def parse_input(contents):
    lines = []
    for fline in contents.splitlines():
        p1, p2 = fline.split(' -> ')
        x1, y1 = list(map(int, p1.split(',')))
        x2, y2 = list(map(int, p2.split(',')))
        lines.append((x1, y1, x2, y2))

    return lines


if __name__ == "__main__":

    lines = parse_input(test)
    print(count_danger(lines))

    print('--- Part 1 ---')
    with open('input.txt') as f:
        lines = parse_input(f.read())

    print(count_danger(lines))
    print('--- Part 2 ---') 
    print(count_danger(lines, diag=True))