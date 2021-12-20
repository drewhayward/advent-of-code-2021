class InfImage:
    DIRS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0,0), (1, 0), (-1, 1), (0, 1), (1,1)]
    def __init__(self, img = None) -> None:
        self.points = set()
        if img is not None:
            for y, row in enumerate(img):
                for x, pixel in enumerate(row):
                    if pixel == '#':
                        self.points.add((x,y))

    def get_pixelnum(self, pos):
        x,y = pos
        b = ''
        for dx, dy in self.DIRS:
            if (x + dx, y + dy) in self.points:
                b += '1'
            else:
                b += '0'

        return int(b, base=2)

    def enhance(self, algo, times=1):
        xmax = max(x for x, y in self.points)
        xmin = min(x for x, y in self.points)
        ymax = max(y for x, y in self.points)
        ymin = min(y for x, y in self.points)

        memo = {}
        def rec_pixel(pos, depth):
            if (depth, pos) not in memo:
                if depth == 1:
                    memo[(depth, pos)] = algo[self.get_pixelnum(pos)]
                else:
                    b = ''
                    x, y = pos
                    for dx, dy in self.DIRS:
                        b += rec_pixel((x + dx, y + dy), depth - 1)
                    
                    memo[(depth, pos)] = algo[int(b, base=2)]

            return memo[(depth, pos)]

        new_points = set()
        for x in range(xmin - times, xmax + times + 1):
            for y in range(ymin - times, ymax + times + 1):
                if rec_pixel((x,y), depth=times) == '1':
                    new_points.add((x,y))

        self.points = new_points

    def __str__(self):
        xmax = max(x for x, y in self.points)
        xmin = min(x for x, y in self.points)
        ymax = max(y for x, y in self.points)
        ymin = min(y for x, y in self.points)
        output = f'({xmin},{ymin})\n'
        for y in range(ymin - 1, ymax + 2):
            for x in range(xmin - 1, xmax + 2):
                if (x,y) in self.points:
                    output += '#'
                else:
                    output += '.'
            output += '\n'
    
        return output

def parse_input(contents):
    enhancement, img = contents.split('\n\n')

    img = [list(line) for line in img.splitlines()]
    enhancement = enhancement.replace('.', '0')
    enhancement = enhancement.replace('#', '1')
    return enhancement, img

if __name__ == "__main__":
    with open('day20/test.txt') as f:
        algo, img = parse_input(f.read()) 

    inf_img = InfImage(img)
    inf_img.enhance(algo,times=2)
    print(len(inf_img.points))
    inf_img = InfImage(img)
    inf_img.enhance(algo,times=50)
    print(len(inf_img.points))

    with open('day20/input.txt') as f:
        algo, img = parse_input(f.read())


    print('--- Part 1 ---')
    inf_img = InfImage(img)
    inf_img.enhance(algo, times=2)
    print(len(inf_img.points))

    print('--- Part 2 ---')
    inf_img = InfImage(img)
    inf_img.enhance(algo, times=50)
    print(len(inf_img.points))