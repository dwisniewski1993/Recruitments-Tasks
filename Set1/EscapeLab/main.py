def can_escape(maze):
    """
    Sprawdza, czy można wyjść z labiryntu od pola (0,0) do pola (9,9).
    Argument:
        maze (list of str): Labirynt opisany jako lista łańcuchów znaków.
    Zwraca:
        int: 1, jeśli można wyjść z labiryntu, 0 w przeciwnym wypadku.
    """
    rows, cols = 10, 10
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def dfs(x, y):
        # Jeżeli wychodzimy poza granice lub trafiamy na zajęte pole, kończymy
        if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] == 'X' or visited[x][y]:
            return False
        # Oznaczamy pole jako odwiedzone
        visited[x][y] = True
        # Jeśli dotarliśmy do wyjścia (9,9), zwracamy True
        if (x, y) == (9, 9):
            return True
        # Przechodzimy do sąsiednich pól (góra, dół, lewo, prawo)
        return dfs(x - 1, y) or dfs(x + 1, y) or dfs(x, y - 1) or dfs(x, y + 1)

    return int(dfs(0, 0))


def main():
    """
    Odczytuje dane wejściowe, sprawdza możliwość wyjścia z każdego labiryntu
    i wypisuje wyniki jako ciąg binarny.
    """
    mazes = []

    while True:
        try:
            line = input().strip()
            if line == '':  # Jeśli linia jest pusta, koniec
                break
            else:
                mazes.append(line)
        except Exception as e:
            print(e)
            break

    results = [can_escape([mazes[i][j:j + 10] for j in range(0, 100, 10)]) for i in range(len(mazes))]
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
