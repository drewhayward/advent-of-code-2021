def inspect(line):
    matched = {'(':')', '[':']', '<':'>', '{':'}'}
    pstack = []
    for c in line:
        if c in matched:
            pstack.append(matched[c])
        elif pstack.pop() != c:
            return 'corrupted', c
        
    if pstack:
        return 'incomplete', pstack
    return 'balanced', None

def score_corrupted(lines):
    scores = {')':3, ']': 57, '}':1197, '>': 25137}
    total = 0
    for line in lines:
        status, c = inspect(line)
        if status == 'corrupted':
            total += scores[c]
    return total

def score_incomplete(lines):
    score_map = {')':1, ']': 2, '}':3, '>': 4}
    scores = []
    for line in lines:
        status, stack = inspect(line)
        if status != 'incomplete': continue

        total = 0
        for c in reversed(stack):
            total = total * 5 + score_map[c]
        scores.append(total)

    scores.sort()
    return scores[len(scores) // 2]

if __name__ == "__main__":
    with open('day10/test.txt') as f:
        test = f.read().splitlines()

    print(score_corrupted(test))
    print(score_incomplete(test))

    print('--- Part 1 ---')
    with open('day10/input.txt') as f:
        lines = f.read().splitlines()

    print(score_corrupted(lines))


    print('--- Part 2 ---')
    print(score_incomplete(lines))