
def step_sub(instrs):
    depth = 0
    pos = 0
    for instr in instrs:
        match instr.split():
            case ['forward', num]:
                pos += int(num)
            case ['down', num]:
                depth += int(num)
            case ['up', num]:
                depth -= int(num)

    return depth, pos

def step_sub2(instrs):
    depth = 0
    pos = 0
    aim = 0
    for instr in instrs:
        match instr.split():
            case ['forward', num]:
                x = int(num)
                pos += x
                depth += aim * x
            case ['down', num]:
                aim += int(num)
            case ['up', num]:
                aim -= int(num)

    return depth, pos

if __name__ == "__main__":
    test = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".splitlines()

    d,p = step_sub(test)
    print(d*p)

    print('---- Part 1 ----')
    with open('input1.txt') as f:
        instructions = f.read().splitlines()
        d,p = step_sub(instructions)
        print(d*p)

    print('---- Part 2 ----')
    d,p = step_sub2(test)
    print(d*p)
    
    d,p = step_sub2(instructions)
    print(d*p)

