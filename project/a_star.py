from heapq import *

# wierzchołki odwiedzone
visited = set()


# funkcja zwracająca wierzchołki do których możemy wejść z wierzchołka node

def neibs(node, matrix):
    result = []

    #  		prawo, dół, lewo, góra
    vectors = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
    ]

    for vec in vectors:

        # dla każego kierunku, oblicza koordynanty wierzch sąsiedniego

        x = vec[0] + node[0]
        y = vec[1] + node[1]

        # warunek sprawdzając, czy nie wychodzimy poza zakres mapy

        if x < 0 or x >= len(matrix):
            continue
        if y < 0 or y >= len(matrix[0]):
            continue

        # sprawdzana zostaje możliwość stanięcia na pole, jeżeli tak to jest to sąsiad

        if matrix[x][y] != '5':
            result.append((x, y))

    # zwracana zostaje lista sąsiadów
    return result


# funkcja heurystyczna
# dając jej koordynanty poczatkowe i koncowe zwracana zostaje odleglosc manhatanska
# traktowana  jako h()

def h_value(node, finish):
    return abs(node[0] - finish[0]) + abs(node[1] - finish[1])


def find_path(matrix):
    # w słowniku prev, dla odwiedzanego wierzch zapamietany zostanie poprzednik
    # za pomoca ktorej zostanie odtworzona droga
    prev = dict()

    # szukanie poczatku oraz konca

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            elem = matrix[i][j]
            if elem == 'P':
                start = (i, j)
            if elem == 'K':
                finish = (i, j)

    # deklaracja kopca

    heap = [(0, 0, start)]
    heapify(heap)

    # deklaracja visited w globalu

    global visited

    # w zmiennej found znajduje sie informacja czy zostala znaleziona jakas sciezka
    found = False

    while True:

        #  funkcja heappop, usuwa  minimalny element z kopca, oraz zwraca nam ten element

        # gdy kopiec bedzie pusty, zostanie wywołany błąd IndexError, w przeciwnym wypadku try

        try:
            #  elementy które trzymane na kolejce są w takiej postaci (dystans, (x, y))

            nothing, distance, node = heappop(heap)

            # warunek sprawdzajacy wierzch koncowy jesli zmiana wartosci i exit z petli

            if node == finish:
                found = True
                break

            # warunek sprawdzajacy, czy wierzch nie został odwiedzony wczesniej, jezeli tak to nie wchodzimy ponownie

            if node in visited:
                continue

            # wierzch zostaje dodany do odwiedzonych

            visited.add(node)

            # dla każdego sąsiada, czyli dla każdej kratki dzielącej bok z naszą
            # aktualną kratką (node)

            for e in neibs(node, matrix):

                # jeśli wierzchołek ten nie został odwiedzony

                if e not in visited:
                    # do e możemy dojść z node dodając relację do słownika

                    prev[e] = node

                    # dodany zostaje ten element do kolejki
                    heappush(
                        heap,
                        (distance + h_value(e, finish) + 1, distance + 1, e)
                    )

        # przechwycenie wyjatku
        except IndexError:
            break

    # jeśli found == False to znaczy, że nie mozna dojsc do konca

    if not found:
        print('Nie znaleziono sciezki!')
        exit(0)

    # odbudowana zostaje ścieżka korzystając z relacji w słowniku prev
    path = []
    while finish != start:
        path.append(finish)
        finish = prev[finish]

    # odwrócenie kolejnosci drogi

    path = path[::-1]

    # zwrócona zostaje  ścieżka, bez startu wiec zostaje dodany
    return [start] + path


# funkcja ta  wczytuje macierz z wejscia
def get_matrix():
    matrix = open('test.in').read()

    matrix = matrix.split('\n')
    matrix = matrix[:-1]
    # bez ostatniej pustej linii
    return matrix


# pobierana jest macierz, która została podana na wejście oraz ścieżka znaleziona przez algorytm
def show_trail(matrix, path):
    print('Mapa:\n')
    for e in matrix:
        for f in e:
            print(f, end='')
        print()

    print('\nZnaleziona sciezka:\n')

    # lista path została przekopiowana do seta, umozliwia to w czasie logarytmicznym zapytania, czy
    # jakiś element jest w zbiorze

    S = set(path)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            x = matrix[i][j]

            if x == 'P' or x == 'K':
                print(x, end='')
            elif (i, j) in S:
                print('x', end='')
            elif (i, j) in visited:
                print('?', end='')
            else:
                print('.', end='')

        # Dla każdej pary koordynantów wypisana zostaje wartosc
        #     - P, jeśli jest to początek
        #     - K, jeśli jest to koniec
        #     - ?, jeśli jest w visited, ale nie jest w path
        #     - x, jeśli jest w path
        #     - ., żadne z powyższych

        print()

    print('\nDroga:\n')
    for e in path:
        print([e[0] + 1, e[1] + 1])


def solve():
    matrix = get_matrix()
    show_trail(matrix, find_path(matrix))


solve()
