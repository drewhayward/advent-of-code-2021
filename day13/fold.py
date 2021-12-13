
def parse_input(contents):
    points, folds = contents.split('\n\n')
    points = [tuple(map(int, p.split(','))) for p in points.split('\n')]

    folds = [line.split()[2].split('=') for line in folds.split('\n')]
    for i in range(len(folds)):
        folds[i][1] = int(folds[i][1])
    return set(points), folds

def fold(points, dir, crease):
    dir = 0 if dir == 'x' else 1
    new_points = set()
    while points:
        point = list(points.pop())
        if point[dir] > crease:
            point[dir] = crease - (point[dir] - crease)

        new_points.add(tuple(point))

    return new_points

def fold_manual(points, folds):
    for dir, crease in folds:
        points = fold(points, dir, crease)
    return points

def print_plane(points):
    y_max = max(points, key=lambda x: x[1])[1]
    x_max = max(points, key=lambda x: x[0])[0]

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if (x, y) in points:
                print('#', end='')
            else:
                print(' ', end='')
        print()

if __name__ == '__main__':
    with open('day13/test.txt') as f:
        points, folds = parse_input(f.read())
    
    print(len(fold(points, folds[0][0], folds[0][1])))

    print('--- Part 1 ---')
    with open('day13/input.txt') as f:
        points, folds = parse_input(f.read())

    print(len(fold(set(points), folds[0][0], folds[0][1])))

    print('--- Part 2 ---')

    points = fold_manual(points, folds)
    print_plane(points) 

    