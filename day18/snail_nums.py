import math
from pprint import pprint
from copy import deepcopy

class Node:
    def __init__(self, n=None, parent = None) -> None:
        self.parent = parent
        if n is None or isinstance(n, int):
            self.n = n
            self.left = None
            self.right = None
            self.children = []
        elif isinstance(n, list):
            self.n = None
            self.left = None
            self.right = None
            self.children = [
                Node(n[0], parent=self),
                Node(n[1], parent=self)]
            if parent is None:
                self._index()

    def magnitude(self):
        if self.n is not None:
            return self.n
        
        return 3 * self.children[0].magnitude() + 2 * self.children[1].magnitude()

    def get_left(self):
        curr = self
        while curr.n is None:
            curr = curr.children[0]
        return curr

    def get_right(self):
        curr = self
        while curr.n is None:
            curr = curr.children[1]
        return curr

    def try_explode(self):
        stack = list((c, 1) for c in reversed(self.children))
        while stack:
            node, depth = stack.pop()

            if node.n is not None and depth >= 5:
                node.parent._explode()
                return True
            stack.extend((c, depth + 1) for c in reversed(node.children))
    
        return False

    def try_split(self):
        curr = self.get_left()
        while curr is not None:
            if curr.n >= 10:
                curr._split()
                return True
        
            curr = curr.right

        return False

    def reduce(self):
        while True:
            # print(self)
            if self.try_explode(): continue
            if self.try_split(): continue
            break

    def _split(self):
        new_node = Node(None, parent = self.parent)
        lchild = Node(math.floor(self.n / 2), parent = new_node)
        rchild = Node(math.ceil(self.n / 2), parent = new_node)
        new_node.children = [lchild, rchild]
        
        if self.parent.children[0] is self:
            self.parent.children[0] = new_node
        else:
            self.parent.children[1] = new_node
            
        self._index()

    def _explode(self):
        new_node = Node(0, parent=self.parent)
        lchild, rchild = self.children
        if lchild.left is not None:
            lchild.left.n += lchild.n

        if rchild.right is not None:
            rchild.right.n += rchild.n

        if self.parent.children[0] is self:
            self.parent.children[0] = new_node
        else:
            self.parent.children[1] = new_node

        self._index()

    def _index(self):
        # move up to root
        root = self
        while root.parent is not None:
            root = root.parent

        prev = None
        stack = list(reversed(root.children))
        while stack:
            node = stack.pop()

            if not node.children:
                node.left = prev
                if prev is not None:
                    prev.right = node
                prev = node
            else:
                stack.extend(reversed(node.children))

    def __add__(self, other):
        new = Node()
        new.children = [deepcopy(self), deepcopy(other)]
        new.children[0].parent = new
        new.children[1].parent = new
        new._index()
        new.reduce()
        return new

    def __str__(self) -> str:
        if not self.children:
            return str(self.n)
            return f"({str(self.n)},{self.depth})"
        else:
            return f'[{str(self.children[0])},{str(self.children[1])}]'

def smart_split(snum):
    stack = 0
    for i, c in enumerate(snum):
        if c == '[':
            stack += 1
        elif c == ']':
            stack -= 1
        elif c == ',' and stack == 0:
            break
    return snum[:i], snum[i + 1:]

def parse_num(snum: str):
    if len(snum) == 1:
        return int(snum)
    return [parse_num(n) for n in smart_split(snum[1:-1])]
        
def part_1(nums):
    num = nums[0]
    for other in nums[1:]:
        num = num + other
    print(num)
    return num.magnitude()

def part_2(nums):
    best = 0
    for a in nums:
        for b in nums:
            best = max(best, (a + b).magnitude())
    
    return best

if __name__ == "__main__":
    with open('day18/test.txt') as f:
        nums = list(map(parse_num, f.read().splitlines()))
        nums = list(map(Node, nums))

    print(part_1(nums))

    print('--- Part 1 ---')
    with open('day18/input.txt') as f:
        nums = list(map(parse_num, f.read().splitlines()))
        nums = list(map(Node, nums))
    
    print(part_1(nums))
    print('--- Part 2 ---')
    print(part_2(nums))