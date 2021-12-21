from itertools import cycle
from copy import deepcopy
from collections import defaultdict

def play_deterministic(p0, p1):
    players = [p0 - 1, p1 - 1]
    scores = [0, 0]
    rolls = 0
    die = iter(cycle(range(1, 101)))
    while scores[0] < 1000 and scores[1] < 1000:
        turn = (rolls // 3) % 2
        turnrolls = (next(die),next(die), next(die))
        players[turn] = (players[turn] + sum(turnrolls)) % 10
        scores[turn] += players[turn] + 1
        rolls += 3

    return rolls * min(scores)

def play_quantum(p0, p1, target=21):
    roll_dist = [(3,1), (4,3), (5,6), (6,7), (7,6), (8,3), (9,1)]
    # Keep track of the number of worlds for each (pos, score) pair
    # (pos, score)
    tabs = [defaultdict(int) for _ in range(2)]
    tabs[0][(p0, 0)] = 1
    tabs[1][(p1, 0)] = 1
    wins = [0,0]

    def unfinished_games(tab):
        unfinished_games = 0
        for pos in range(10 + 1):
            for score in range(target + 1):
                unfinished_games += tab[(pos, score)]
        return unfinished_games

    turn = 0
    while unfinished_games(tabs[0]) != 0 and unfinished_games(tabs[1]) != 0:
        opponent = 1 - turn
        newtab = defaultdict(int)
        for pos, score in tabs[turn]:
                worlds = tabs[turn][(pos, score)]
                if worlds == 0: continue

                for roll, times in roll_dist:
                    newpos = ((pos + roll - 1 ) % 10) + 1
                    newscore = min(score + newpos, target)
                    newtab[(newpos, newscore)] += worlds * times

        # add wins and remove those winning games
        for pos in range(10 + 1):
            # Each winning score could beat ANY of the unfinished games
            # for the opponent
            wins[turn] += newtab[(pos, target)] * unfinished_games(tabs[opponent])
            del newtab[(pos, target)]

        tabs[turn] = newtab
        turn = opponent

    return max(wins)

if __name__ == "__main__":
    p0, p1 = 4, 8

    print(play_deterministic(p0, p1))
    print(play_quantum(p0, p1))
    print('--- Part 1 ---')
    print(play_deterministic(8,7))
    print('--- Part 2 ---')
    print(play_quantum(8,7, target=21))