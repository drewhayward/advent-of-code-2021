from collections import Counter, defaultdict
import numpy as np
import matplotlib.pyplot as plt
import cProfile

def fit_homography(P1, P2):
    # p is a size (N, 3) set of 3d points
    # X is a size (N, 4) set of 3d points

    N, _ = P1.shape
    M = np.zeros((N*3, 12))
    b = np.zeros((N*3, 1))
    for i, (p, y) in enumerate(zip(P1, P2)):
        b[i*3:i*3+3, 0] = y

        M[i*3, :3] = p
        M[i*3 + 1, 3:6] = p
        M[i*3 + 2, 6:9] = p

        M[i*3: i*3 + 3, 9:] = np.eye(3)

    x = np.linalg.inv(M.T @ M) @ M.T @ b

    R = x[:9].reshape(3,3).round().astype(int)
    t = x[9:].round().astype(int)
    return R, t

class SensorData:
    def __init__(self, points: np.ndarray):
        self.points = points
        self.point_to_dists = defaultdict(set)

        self.sensors = np.zeros((1,3))

        # Get dists for points
        self._find_dists()
    
    def _find_dists(self):
        self.point_to_dists = defaultdict(set)
        for p1 in self.points:
            for p2 in self.points:
                if tuple(p1) == tuple(p2): continue
                d = ((p1 - p2) ** 2).sum().item()
                self.point_to_dists[tuple(p1)].add(d)
                self.point_to_dists[tuple(p2)].add(d)

    def add_points(self, other):
        matches = self.match_points(other)
        
        if matches is None or matches.shape[0] < 12:
            return False

        P1, P2 = self.points[matches[:,0], :], other.points[matches[:,1], :]
        
        R, t = fit_homography(P2, P1)

        transformed = other.points @ R.T + t.T

        self.points = np.concatenate([self.points, transformed])
        self.points = np.unique(self.points, axis=0)
        # self._find_dists()
        for new_point, old_point in zip(transformed, other.points):
            self.point_to_dists[tuple(new_point)].update(other.point_to_dists[tuple(old_point)])

        # Also map the sensor location to store list of sensors
        self.sensors = np.concatenate([
            self.sensors,
            other.sensors @ R.T + t.T
        ])

        return True

    def match_points(self, other):
        paired = []
        for j, p2 in enumerate(other.points):
            for i, p1 in enumerate(self.points):
                dists1 = self.point_to_dists[tuple(p1)]
                dists2 = other.point_to_dists[tuple(p2)]
                common = dists1.intersection(dists2)
                
                if len(common) < 11: continue
                
                paired.append((i, j))
            
            if len(paired) == 12:
                break

        if not paired: return None

        return np.stack(paired)

    def max_dist(self):
        best = 0
        for s1 in self.sensors:
            for s2 in self.sensors:
                d = np.abs(s1 - s2).sum().item()

                best = max(d, best)
        return int(best)

def parse_input(contents):
    sensors = contents.split('\n\n')

    output = []
    for sensor in sensors:
        output.append(
            np.stack(
                [list(map(int, line.split(',')))
                for line in sensor.splitlines()[1:]]
            )
        )

    return output

def vis_cloud(points):
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z)
    plt.show()

def part_1(sensors):
    sensors = [SensorData(np.copy(n)) for n in sensors]

    data = sensors[0]
    to_pair = set(range(1, len(sensors)))
    while to_pair:
        again = set()
        for i in to_pair:
            if data.add_points(sensors[i]): continue
            again.add(i)

        to_pair = again

    return data

if __name__ == "__main__":
    with open('day19/test.txt') as f:
        sensors = parse_input(f.read())

    data = part_1(sensors)
    print(data.points.shape[0])
    print(data.max_dist())

    print('--- Part 1 ---')
    with open('day19/input.txt') as f:
        sensors = parse_input(f.read())

    data = part_1(sensors)
    print(data.points.shape[0])

    print('--- Part 2 ---')
    print(data.max_dist())