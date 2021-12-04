import re
from pprint import pprint
from functools import reduce
import operator
test = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def parse_input(contents):
    nums, *boards = contents.split('\n\n')

    nums = list(map(int, nums.split(',')))
    boards = [[[int(num) for num in row.split()] for row in board.split('\n')] for board in boards]

    return nums, boards

def check_board(board):
    r = any(all(n is None for n in row) for row in board)
    c = any(all(board[i][j] is None for i in range(len(board))) for j in range(len(board)))
    return r or c

def update_board(board, num):
    for i, row in enumerate(board):
        for j, bnum in enumerate(row):
            if bnum == num:
                board[i][j] = None
                if check_board(board):
                    return True
    return False


def run_bingo(nums, boards):
    for num in nums:
        for board in boards:
            if update_board(board, num):
                return sum([n for row in board for n in row if n is not None]) * num
                
def run_backwards_bingo(nums, boards):
    next_boards = boards
    for num in nums:
        curr_boards = next_boards
        next_boards = []

        for board in curr_boards:
            if not update_board(board, num):
                next_boards.append(board)
            elif len(curr_boards) == 1:
                return sum([n for row in board for n in row if n is not None]) * num


if __name__ == "__main__":

    nums, boards = parse_input(test)
    print(nums)
    for board in boards:
        pprint(board)

    print('Test:')
    print(run_bingo(nums, boards))

    print('--- Part 1 ---')
    with open('input.txt') as f:
        nums, boards = parse_input(f.read())
        print(run_bingo(nums, boards))


    print('--- Part 2 ---')
    print(run_backwards_bingo(nums, boards))