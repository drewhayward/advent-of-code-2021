from itertools import product, pairwise

def span_overlap(a, b):
    return not (a[0] >= b[1] or a[1] <= b[0])

def span_subsumes(a, b):
    # a subsumes b
    return (a[0] <= b[0] < a[1]) and (a[0] <= b[1] <= a[1])

def get_subspans(a, b):
    # when finding the cublets of a cube, this finds only the smallest possible
    # ones which cover the orginal span but don't overlap
    points = set(filter(lambda x: a[0] <= x <= a[1], a + b))
    points = sorted(list(points))
    return pairwise(points)
    
def volume(cube):
    return max(0, cube[1] - cube[0]) * max(0, cube[3] - cube[2]) * max(0, cube[5] - cube[4])

def cube_overlaps(cube1, cube2):
    return all([
        span_overlap(cube1[:2], cube2[:2]),
        span_overlap(cube1[2:4], cube2[2:4]),
        span_overlap(cube1[4:], cube2[4:]),
    ])

def fracture_by(cube1, cube2):
    if not cube_overlaps(cube1, cube2): return [cube1]

    # Find all subcubes that could be created by the other cube
    xsides = get_subspans(cube1[:2], cube2[:2])
    ysides = get_subspans(cube1[2:4], cube2[2:4])
    zsides = get_subspans(cube1[4:], cube2[4:])

    subcubes = set()
    for xside, yside, zside in product(xsides, ysides, zsides):
        subcube = (*xside, *yside, *zside)
        # if this cube has no volume, skip
        volume = max(0, xside[1] - xside[0]) * max(0, yside[1] - yside[0]) * max(0, zside[1] - zside[0])
        if volume == 0: continue

        subcubes.add(subcube)

    return subcubes

def track_cubes(instructions, filter=False):
    cubes = set()
    for is_on, cube in instructions:
        if filter and not(-50 <= cube[0] <= 50): continue

        if is_on: # add cube
            to_add = {cube}
            to_remove = set()
            for tcube in cubes:
                if not cube_overlaps(tcube, cube): continue
                pieces = fracture_by(tcube, cube)
                to_add.update(pieces.difference(fracture_by(cube, tcube)))
                to_remove.add(tcube)
            
            cubes.difference_update(to_remove)
            cubes.update(to_add)
        else: # subtract cube
            to_add = set()
            to_remove = set()
            for mcube in cubes:
                if not cube_overlaps(mcube, cube): continue
                to_remove.add(mcube) # remove this larger cube

                # Nontrivial intersection
                fractured = fracture_by(mcube, cube).difference(fracture_by(cube, mcube))
                to_add.update(fractured)
                
            cubes.difference_update(to_remove)
            cubes.update(to_add)

    return sum(map(volume, cubes))

def parse_input(contents):
    cuboids = []
    for line in contents.splitlines():
        io, coords = line.split(' ')
        bounds = []
        for cord in coords.split(','):
            bounds.extend(map(int, cord[2:].split('..')))
        bounds[1] += 1
        bounds[3] += 1
        bounds[5] += 1

        cuboids.append((io == 'on', tuple(bounds)))

    return cuboids

if __name__ == "__main__":
    with open('day22/test.txt') as f:
        instructions = parse_input(f.read())
    
    print(track_cubes(instructions, filter=False))

    with open('day22/input.txt') as f:
        instructions = parse_input(f.read())

    print('--- Part 1 ---')
    print(track_cubes(instructions, filter=True))
    print('--- Part 2 ---')
    print(track_cubes(instructions, filter=False))
