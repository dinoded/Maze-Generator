import random
from collections import deque

def generate_labyrinth_with_thin_walls(size=10):
    # Создаем лабиринт с 4 стенами для каждой ячейки
    labyrinth = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]  # [right_wall, bottom_wall, left_wall, top_wall]

    def carve_passages_from(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < size and 0 <= ny < size and all(labyrinth[nx][ny]):
                if dx == 0 and dy == 1:  # Right
                    labyrinth[cx][cy][0] = 0
                    labyrinth[nx][ny][2] = 0
                elif dx == 1 and dy == 0:  # Down
                    labyrinth[cx][cy][1] = 0
                    labyrinth[nx][ny][3] = 0
                elif dx == 0 and dy == -1:  # Left
                    labyrinth[cx][cy][2] = 0
                    labyrinth[nx][ny][0] = 0
                elif dx == -1 and dy == 0:  # Up
                    labyrinth[cx][cy][3] = 0
                    labyrinth[nx][ny][1] = 0
                carve_passages_from(nx, ny)

    carve_passages_from(0, 0)
    return labyrinth

def ensure_path_exists(labyrinth, start, end):
    size = len(labyrinth)
    stack = [start]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return
        visited.add((x, y))
        for i, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited:
                if labyrinth[x][y][i] == 0:
                    stack.append((nx, ny))

    # Если пути нет, создаем его
    x, y = start
    while (x, y) != end:
        if x < end[0]:
            labyrinth[x][y][1] = 0
            labyrinth[x + 1][y][3] = 0
            x += 1
        elif x > end[0]:
            labyrinth[x][y][3] = 0
            labyrinth[x - 1][y][1] = 0
            x -= 1
        elif y < end[1]:
            labyrinth[x][y][0] = 0
            labyrinth[x][y + 1][2] = 0
            y += 1
        elif y > end[1]:
            labyrinth[x][y][2] = 0
            labyrinth[x][y - 1][0] = 0
            y -= 1

def place_start_and_end(labyrinth):
    size = len(labyrinth)
    start = (0, 0)
    end = (size - 1, size - 1)
    return start, end

def place_letters(labyrinth, count=4):
    size = len(labyrinth)
    letters = []
    while len(letters) < count:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if (x, y) not in letters and (x, y) != (0, 0) and (x, y) != (size - 1, size - 1):
            letters.append((x, y))
    return letters

def print_labyrinth(labyrinth, start, end, letters, path=None):
    size = len(labyrinth)
    path_set = set(path) if path else set()
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    for y in range(size):
        # Print top walls
        for x in range(size):
            print("█" if labyrinth[x][y][3] else " ", end="█")
        print()  # End of row top
        # Print cells and right walls
        for x in range(size):
            if (x, y) == start:
                print(f"{GREEN}S{RESET}", end="")
            elif (x, y) == end:
                print(f"{RED}K{RESET}", end="")
            elif (x, y) in path_set:
                print(f"{GREEN}*{RESET}", end="")
            elif (x, y) in letters:
                print("L", end="")
            else:
                print(" ", end="")
            print("█" if labyrinth[x][y][0] else " ", end="")

        print()
    # Print bottom walls of last row
    for x in range(size):
        print("█" if labyrinth[x][size - 1][1] else " ", end="█")
    print()

def find_shortest_path(labyrinth, start, end):
    size = len(labyrinth)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path + [(x, y)]

        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited:
                if labyrinth[x][y][i] == 0:  # Check if wall is open
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(x, y)]))

    return None

def main():
    size = 10  # Square labyrinth
    labyrinth = generate_labyrinth_with_thin_walls(size)
    start, end = place_start_and_end(labyrinth)
    ensure_path_exists(labyrinth, start, end)
    letters = place_letters(labyrinth, count=4)

    path = find_shortest_path(labyrinth, start, end)

    print("Labirynt z literami:")
    print_labyrinth(labyrinth, start, end, letters, path)

    print(f"\nPunkt startowy: {start}, Punkt końcowy: {end}")
    print(f"Litery do zebrania: {letters}")

    if path:
        print("\nIstnieje ścieżka z punktu S do K.")
        print(f"Długość najkrótszej ścieżki: {len(path) - 1}")
        print("Ścieżка:", path)
    else:
        print("\nNie istnieje ścieżka z punktu S do K.")

if __name__ == "__main__":
    main()
