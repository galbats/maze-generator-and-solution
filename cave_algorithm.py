import random

def initialize_cave(rows, cols, initial_chance):
    """Инициализация пещеры: каждая клетка с вероятностью `initial_chance` становится "живой" (1)."""
    return [[1 if random.random() < initial_chance else 0 for _ in range(cols)] for _ in range(rows)]

def count_alive_neighbors(cave, i, j, rows, cols):
    """Подсчет количества соседей, которые являются "живыми"."""
    alive = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue  # Пропускаем саму клетку
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                alive += cave[ni][nj]
            else:
                alive += 1  # Клетки за границей считаются "живыми"
    return alive

def update_cave(cave, birth_limit, death_limit):
    """Один шаг клеточного автомата: обновление состояния пещеры."""
    rows, cols = len(cave), len(cave[0])
    new_cave = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            alive_neighbors = count_alive_neighbors(cave, i, j, rows, cols)
            if cave[i][j] == 1:
                # "Живая" клетка умирает, если соседей меньше, чем death_limit
                new_cave[i][j] = 1 if alive_neighbors >= death_limit else 0
            else:
                # "Мёртвая" клетка оживает, если соседей больше или равно birth_limit
                new_cave[i][j] = 1 if alive_neighbors > birth_limit else 0

    return new_cave

def load_cave_from_file(file_path):
    """Загрузка пещеры из файла."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    rows, cols = map(int, lines[0].strip().split())
    cave = [list(map(int, line.strip().split())) for line in lines[1:]]
    return rows, cols, cave

def save_cave_to_file(file_path, cave):
    """Сохранение пещеры в файл."""
    with open(file_path, 'w') as f:
        rows, cols = len(cave), len(cave[0])
        f.write(f"{rows} {cols}\n")
        for row in cave:
            f.write(" ".join(map(str, row)) + "\n")
