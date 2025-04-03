# your code goes here
import numpy as np


def main():
    t = int(input())
    all_tests = []

    for _ in range(t):
        n = int(input())
        points = []

        for _ in range(n):
            line = input().split()
            name = line[0]
            x = int(line[1])
            y = int(line[2])
            points.append((name, x, y))

        all_tests.append(points)

    for i, points in enumerate(all_tests):
        coords = np.array([[p[1], p[2]] for p in points])

        distances = np.sqrt(np.sum(coords ** 2, axis=1))

        sorted_points = [points[i] for i in np.argsort(distances)]

        for point in sorted_points:
            print(f"{point[0]} {point[1]} {point[2]}")

        if i < len(all_tests) - 1:
            print()


if __name__ == "__main__":
    main()
