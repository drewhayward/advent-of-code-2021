import math
from itertools import product
import tqdm

def parse_input(s):
    x,y = s[13:].split(', ')
    xlo, xhi = list(map(int, x[2:].split('..')))
    ylo, yhi = list(map(int, y[2:].split('..')))
    
    return xlo, xhi, ylo, yhi

def inbounds(pos, bounds):
    x, y = pos
    xlo, xhi, ylo, yhi = bounds
    return xlo <= x <= xhi and ylo <= y <= yhi

def y_intercepts(v_0, y):
    a = -1
    b = (2*v_0 + 1)
    c = -2*y

    r1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a) # Going up
    r2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a) # Going down
    return r1, r1

def find_highest(bounds):
    _, _, ylo, yhi = bounds
    # best = 0
    # for vy in range(ylo, max(abs(yhi), abs(ylo))):
    #     t_lo_up, t_lo_down = y_intercepts(vy, ylo)
    #     t_hi_up, t_hi_down = y_intercepts(vy, yhi)

    #     # Does it hit on the way up?
    #     hit_upwards = math.ceil(t_lo_up) <= math.floor(t_lo_down)

    #     # Does it hit on the way down?
    #     hit_downwards = math.ceil(t_hi_down) <= math.floor(t_hi_up)

    #     if hit_upwards or hit_downwards:
    #         best = max(best, vy * (vy + 1) / 2)

    a = max(abs(ylo), abs(yhi))
    return int(a * (a - 1) / 2)

def find_points(bounds):
    xlo, xhi, ylo, yhi = bounds

    count = 0
    vx_lower_bound = math.ceil((-1 + math.sqrt(1 + 8 * xlo)) / 2)
    vy_upper_bound = max(abs(yhi), abs(ylo))
    for vx, vy in product(range(vx_lower_bound, xhi + 1), range(ylo, vy_upper_bound + 1)):
        for t in range(1, 1000):
            # Set X component
            if t >= vx:
                x = vx * (vx + 1) / 2
            else:
                d = vx - t
                x = vx * (vx + 1) / 2 - d * (d + 1) / 2

            # Set Y Component
            if t <= vy:
                d = vy - t
                y = vy * (vy + 1) / 2 - d * (d + 1) / 2
            else: 
                d = t - vy - 1
                y = vy * (vy + 1) / 2 - d * (d + 1) / 2

            if inbounds((x, y), bounds):
                count += 1
                break

    return count


if __name__ == "__main__":
    bounds = parse_input("target area: x=20..30, y=-10..-5")

    print(find_highest(bounds))
    print(find_points(bounds))

    print('--- Part 1 ---')
    bounds = parse_input("target area: x=25..67, y=-260..-200")
    print(find_highest(bounds))

    print('--- Part 2 ---')
    print(find_points(bounds))
