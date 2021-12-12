from collections import defaultdict, Counter

class History(Counter):
    def __init__(self, max_repeats=2):
        super().__init__()
        self.max_repeats = max_repeats
        self.repeated_node = None

    def __setitem__(self, k, v) -> None:
        super().__setitem__(k, v)
        if v == self.max_repeats:
            self.repeated_node = k
        elif k == self.repeated_node:
            self.repeated_node = None
        return v

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
    res = _count('start', [])
    return res

def count_paths2(adj):
    # Counts the number of ways to the 'end' node from the 'node' given the 
    # history
    def _count(node, history, stack): 
        if node == 'end':
            return 1

        total = 0
        if node.islower() and node != 'start':
            history[node] += 1
        for neighbor in adj[node]:
            if neighbor == 'start': continue
            # Not allowed to revisit lowercase nodes
            if neighbor.islower() and neighbor in history and history.repeated_node is not None:
                continue 
            
            total += _count(neighbor, history, stack)
        if node.islower() and node != 'start':
            history[node] -= 1 
            if history[node] <= 0:
                del history[node]
        return total
    res = _count('start', History(), [])
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