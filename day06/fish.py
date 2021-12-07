from collections import Counter

test = """3,4,3,1,2"""

def parse_input(contents):
    return Counter(map(int, contents.split(',')))

def simulate_fish(ctr, days: int):
    
    new_ctr = Counter()
    for _ in range(days):
        for num, fish in ctr.items():
            if num != 0:
                new_ctr[num - 1] += fish
            else:
                new_ctr[8] += fish
                new_ctr[6] += fish

        ctr = new_ctr
        new_ctr = Counter()

    return sum(ctr.values())

if __name__ == "__main__":
    ctr = parse_input(test)
    print(simulate_fish(ctr, 80))

    print(simulate_fish(ctr, 256))

    print('--- Part 1 ---')
    with open('input.txt') as f:
        ctr = parse_input(f.read())

    print(simulate_fish(ctr, 80))

    print('--- Part 2 ---')
    print(simulate_fish(ctr, 256))