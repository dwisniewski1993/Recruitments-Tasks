def roman_to_arabic(roman):
    """Konwertuje liczbę rzymską na arabską."""
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    arabic = 0
    prev_value = 0

    # Iterujemy od końca, aby łatwiej obsłużyć odjęcia (np. IV to 5-1=4)
    for char in reversed(roman):
        value = roman_values[char]

        # Jeśli aktualna wartość jest mniejsza od poprzedniej, odejmujemy
        if value < prev_value:
            arabic -= value
        else:
            arabic += value

        prev_value = value

    return arabic


def arabic_to_roman(arabic):
    """Konwertuje liczbę arabską na rzymską."""
    # Lista par (wartość arabska, odpowiednik rzymski) w kolejności malejącej
    roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    roman = ''

    for value, numeral in roman_map:
        while arabic >= value:
            roman += numeral
            arabic -= value

    return roman


def main():
    # Lista na przechowywanie wszystkich wyników
    results = []

    # Wczytujemy dane wejściowe linia po linii aż do końca pliku
    while True:
        try:
            line = input().strip()
            if line == '':  # Jeśli linia jest pusta, pomijamy
                break

            # Dzielimy linię na dwie liczby rzymskie
            first_roman, second_roman = line.split()

            # Konwertujemy liczby rzymskie na arabskie, dodajemy i konwertujemy wynik z powrotem na liczbę rzymską
            first_arabic = roman_to_arabic(first_roman)
            second_arabic = roman_to_arabic(second_roman)
            sum_arabic = first_arabic + second_arabic
            sum_roman = arabic_to_roman(sum_arabic)

            # Dodajemy wynik do listy
            results.append(sum_roman)

        except EOFError:
            break  # Koniec pliku wejściowego

    # Wyświetlamy wszystkie wyniki na końcu
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
