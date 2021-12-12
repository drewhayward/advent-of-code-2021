from collections import defaultdict, Counter

def count_paths(adj):
    
    # Counts the number of ways to the 'end' node from the 'node' given the 
    # history
    def _count(node, history): 
        if node == 'end':
            return 1

        total = 0
        history.append(node)
        for neighbor in adj[node]:
            # Not allowed to revisit lowercase nodes
            if neighbor.islower() and neighbor in history:
                continue 
            
            total += _count(neighbor, history)
        history.pop()
        return total
    return _count('start', [])

def count_paths2(adj):
    # Counts the number of ways to the 'end' node from the 'node' given the 
    # history
    def _count(node, history=[], repeat=False): 
        if node == 'end':
            return 1

        total = 0
        history.append(node)
        for neighbor in adj[node]:
            if neighbor == 'start': continue
            
            if neighbor.islower():
                c = history.count(neighbor)
                if c == 1 and not repeat:
                    total += _count(neighbor, history, True)
                elif c == 0:
                    total += _count(neighbor, history, repeat)
            else:
                total += _count(neighbor, history, repeat)
        history.pop()
        return total
    res = _count('start')
    return res

def parse_input(contents):
    adj = defaultdict(list)
    for line in contents.splitlines():
        k, v = line.split('-')
        adj[k].append(v)
        adj[v].append(k)
    return adj

if __name__ == "__main__":
    test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    adj = parse_input(test)
    print(count_paths(adj))
    print(count_paths2(adj))

    print('--- Part 1 ---')
    with open('day12/input.txt') as f:
        adj = parse_input(f.read())
    print(count_paths(adj))

    print('--- Part 2 ---')
    print(count_paths2(adj))