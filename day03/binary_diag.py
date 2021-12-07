from operator import ge, lt

def count_ones(bins):
    counter = [0 for _ in next(iter(bins))]
    for num in bins:
        for i, bit in enumerate(num):
            if bit == '1':
                counter[i] += 1
    return counter

def gamma_epsilon(bins):
    counter = count_ones(bins)
    gamma = int(''.join(['1' if c > len(bins) // 2 else '0' for c in counter]), base=2)
    epsilon = gamma ^ (2**(len(bins[0])) - 1)

    return gamma, epsilon

def life_support(bins, comp):
    counter = count_ones(bins)

    pos = 0
    curr_nums = set(bins)
    next_nums = set()
    while len(curr_nums) > 1:
        if comp(counter[pos], (len(curr_nums) / 2)):
            mcb = '1'
        else:
            mcb = '0'

        for num in curr_nums:
            if num[pos] == mcb:
                next_nums.add(num)
        
        curr_nums = next_nums
        next_nums = set()
        counter = count_ones(curr_nums)
        pos += 1
    num = list(curr_nums)[0]
    return int(num, base=2)


if __name__ == "__main__":
    test = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines()
    
    g,e = gamma_epsilon(test)
    print(g*e)

    print('---- Part 1 ----')
    with open('input1.txt') as f:
        bins = f.read().splitlines()

        g, e = gamma_epsilon(bins)
        print(g*e)
    
    print('---- Part 2 ----')
    life_support_oxy = lambda x: life_support(x, ge)
    life_support_co2 = lambda x: life_support(x, lt)
    print(life_support_oxy(test) * life_support_co2(test))

    print(life_support_oxy(bins) * life_support_co2(bins))