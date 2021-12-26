from pprint import pprint


def step_floor(seafloor):
    newfloor = list(map(list, seafloor))
    # East
    for y, row in enumerate(seafloor):
        for x, cell in enumerate(row):
            if cell != '>': continue

            next_x = (x + 1) % len(seafloor[0])
            if seafloor[y][next_x] == '.':
                newfloor[y][next_x] = '>'
                newfloor[y][x] = '.'

    seafloor = tuple(map(tuple, newfloor))
    newfloor = list(map(list, seafloor))

    # South
    for y in range(len(seafloor) - 1, -1, -1):
        row = seafloor[y]
        for x, cell in enumerate(row):
            if cell != 'v': continue

            next_y = (y + 1) % len(seafloor)
            if seafloor[next_y][x] == '.':
                newfloor[next_y][x] = 'v'
                newfloor[y][x] = '.'

    return tuple(map(tuple, newfloor))

def find_halt(seafloor):
    prevfloor = None
    step = 1
    # print_floor(seafloor)
    while prevfloor != seafloor:
        # print('---')
        prevfloor = seafloor
        seafloor = step_floor(seafloor)
        step += 1
        # print_floor(seafloor)

    return step - 1

def print_floor(sfloor):
    for row in sfloor:
        print(''.join(row))


if __name__ == "__main__":
    test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

    seafloor = tuple(map(tuple, test.splitlines()))

    print(find_halt(seafloor))

    with open('day25/input.txt') as f:
        seafloor = tuple(map(tuple, f.read().splitlines()))


    print('--- Part 1 ---')
    print(find_halt(seafloor))