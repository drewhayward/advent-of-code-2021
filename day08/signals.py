from collections import Counter
from itertools import permutations

letters = set('abcdefg')
nums = {1,2,3,4,5,6,7,8,9,0}

true_map = {
    '0':'abcefg',
    '1':'cf',
    '2':'acdeg',
    '3':'acdfg',
    '4':'bcdf',
    '5':'abdfg',
    '6':'abdefg',
    '7':'acf',
    '8':'abcdefg', 
    '9': 'abcdfg'
}
inv_true_map = {v:k for k,v in true_map.items()}

def parse_input(contents):
    lines = contents.splitlines()
    segments = []
    for line in lines:
        samples, digits = line.split(' | ')
        samples = samples.split()
        digits = digits.split()

        segments.append((samples, digits))
    
    return segments

def count_unique(segs):
    total = 0
    for _, digits in segs:
        for digit in digits:
            if len(digit) in {2,3,4,7}:
                total += 1
    return total

def decipher_signal(signals, digits):
    # BRUTE FORCE
    real_digits = set(true_map.values())

    # map
    def caesar_norm(s, caesar):
        return ''.join((sorted([caesar[c] for c in s])))

    for perm in permutations('abcdefg'):
        caesar = {c: p for c, p in zip(perm, 'abcdefg')}
        candidate = set(caesar_norm(s, caesar) for s in signals)

        if len(real_digits.intersection(candidate)) == 10:
            break

    # Map digits
    res = ''
    for digit in digits:
        res += inv_true_map[caesar_norm(digit, caesar)]
    
    return int(res)
def decipher_signals(segs):
    total = 0
    for sig, digs in segs:
        total += decipher_signal(sig, digs)

    return total


if __name__ == "__main__":
    with open('day08/testinput.txt') as f:
        test_segments = parse_input(f.read())

    print(count_unique(test_segments))


    print('---- Part 1 ----')
    with open('day08/input.txt') as f:
        segs = parse_input(f.read())

    print(count_unique(segs))

    print('--- Part 2 ---')
    print(decipher_signals(segs))