from collections import Counter
from itertools import pairwise

def parse_input(contents):
    template, rules = contents.split('\n\n')

    insertions = {}
    for rule in rules.splitlines():
        lhs, rhs = rule.split(' -> ')
        insertions[tuple(lhs)] = rhs
    
    return template, insertions

def efficient_expansion(poly, rules, steps):
    char_counts = Counter(poly)
    pair_counts = Counter(pairwise(poly))

    for _ in range(steps):
        new_pair_counts = Counter(pair_counts)
        for pair, c in pair_counts.items():
            # Keep track of the single chars
            if pair in rules:
                insert_char = rules[pair]
                char_counts[insert_char] += c

                new_pair_counts[(pair[0], insert_char)] += c
                new_pair_counts[(insert_char, pair[1])] += c
                new_pair_counts[pair] -= c

        pair_counts = new_pair_counts

    return max(char_counts.values()) - min(char_counts.values())

if __name__ == "__main__":
    with open('day14/test.txt') as f:
        template, rules = parse_input(f.read())

    print(efficient_expansion(template, rules, 10))
    
    with open('day14/input.txt') as f:
        template, rules = parse_input(f.read())

    print('--- Part 1 ---')
    print(efficient_expansion(template, rules, 10))
    print('--- Part 2 ---')
    print(efficient_expansion(template, rules, 40))