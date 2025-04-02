from numba import njit
import sys
import math
import numpy as np

@njit
def simple_sieve(limit):
    is_prime = np.ones(limit + 1, dtype=np.uint8)  # Używamy uint8 dla oszczędności pamięci
    is_prime[0] = is_prime[1] = 0  # 0 i 1 nie są pierwsze

    for start in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[start]:
            for multiple in range(start * start, limit + 1, start):
                is_prime[multiple] = 0  # Oznaczamy wielokrotności jako niepierwsze

    return np.where(is_prime == 1)[0]  # Zwracamy tablicę NumPy z liczbami pierwszymi

@njit
def segmented_sieve(m, n):
    limit = int(math.sqrt(n)) + 1
    primes = simple_sieve(limit)

    is_prime = np.ones(n - m + 1, dtype=np.uint8)

    for prime in primes:
        start = max(prime * prime, m + (prime - m % prime) % prime)
        for multiple in range(start, n + 1, prime):
            is_prime[multiple - m] = 0  # Oznaczamy wielokrotności jako niepierwsze

    if m == 1:
        is_prime[0] = 0  # 1 nie jest liczbą pierwszą

    return np.where(is_prime == 1)[0] + m  # Zwracamy liczby pierwsze przesunięte o `m`

def main():
    t = int(sys.stdin.readline().strip())
    results = []

    for _ in range(t):
        m, n = map(int, sys.stdin.readline().split())
        primes = segmented_sieve(m, n)
        results.append('\n'.join(map(str, primes)))

    print('\n\n'.join(results))

if __name__ == "__main__":
    main()
