def count_neighbors(board, row, col):
    """Liczy żywych sąsiadów dla danej komórki, uwzględniając toroidalną planszę 5x5"""
    count = 0
    rows, cols = len(board), len(board[0])

    # Sprawdź wszystkich 8 sąsiadów
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            # Obliczamy współrzędne sąsiada z uwzględnieniem zawijania planszy
            neighbor_row = (row + dr) % rows
            neighbor_col = (col + dc) % cols

            count += board[neighbor_row][neighbor_col]

    return count


def next_generation(board):
    """Generuje następny stan planszy według zasad gry w życie"""
    rows, cols = len(board), len(board[0])
    new_board = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            neighbors = count_neighbors(board, row, col)

            # Reguły przejścia do następnego stanu
            if board[row][col] == 1:
                new_board[row][col] = 1 if 2 <= neighbors <= 3 else 0
            else:
                new_board[row][col] = 1 if neighbors == 3 else 0

    return new_board


def simulate_game(initial_board, steps=100):
    """Symuluje grę w życie przez określoną liczbę kroków"""
    board = initial_board

    for _ in range(steps):
        board = next_generation(board)

        # Optymalizacja: jeśli wszystkie komórki są martwe, dalsze kroki nic nie zmienią
        if all(cell == 0 for row in board for cell in row):
            return False

    return any(cell == 1 for row in board for cell in row)


def parse_input():
    """Parsuje dane wejściowe i zwraca wyniki dla wszystkich testów"""
    n = int(input())
    results = []

    for _ in range(n):
        # Wczytaj planszę 5x5
        board = [list(map(int, input().strip())) for _ in range(5)]

        # Symuluj grę i zapisz wynik
        has_living_cells = simulate_game(board)
        results.append("yes" if has_living_cells else "no")

    return results


def main():
    results = parse_input()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()