import sys
import numpy as np


def reverse_array():
    t = int(sys.stdin.readline().strip())  # Wczytujemy liczbę testów
    results = []

    for _ in range(t):
        data = np.array(list(map(int, sys.stdin.readline().split())))  # Wczytujemy dane jako numpy array
        n, arr = data[0], data[1:]  # Pierwsza liczba to n, reszta to tablica
        results.append(" ".join(map(str, arr[::-1])))  # Odwracamy tablicę i formatujemy wynik

    print("\n".join(results))  # Wypisujemy wyniki dla wszystkich testów


if __name__ == "__main__":
    reverse_array()  # Uruchamiamy funkcję
