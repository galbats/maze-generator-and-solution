from collections import deque

def load_maze_from_file(file_path):
    # Загрузка лабиринта из файла
    with open(file_path, 'r') as f:
        lines = f.readlines()

    rows, cols = map(int, lines[0].strip().split())  # Чтение размеров лабиринта

    vertical_walls = []
    # Чтение вертикальных стен
    for i in range(rows):
        vertical_walls.append([1 - int(x) for x in lines[1 + i].strip().split()])

    horizontal_walls = []
    # Чтение горизонтальных стен
    for i in range(rows):
        horizontal_walls.append([1 - int(x) for x in lines[1 + rows + 1 + i].strip().split()])

    return rows, cols, vertical_walls, horizontal_walls  # Возвращаем данные лабиринта

def bfs_solve(maze, start, goal, vertical_walls, horizontal_walls):
    # Решение лабиринта с помощью алгоритма BFS
    rows, cols = len(vertical_walls), len(vertical_walls[0])  # Размеры лабиринта
    queue = deque([start])  # Очередь для обхода
    visited = {start: None}  # Хранение посещенных ячеек

    while queue:
        current = queue.popleft()  # Текущая ячейка
        if current == goal:
            break  # Остановка, если найдена цель

        x, y = current
        neighbors = []

        # Проверка соседей (вверх, вниз, влево, вправо)
        if y > 0 and horizontal_walls[y-1][x] == 1 and (x, y-1) not in visited:
            neighbors.append((x, y-1))
        if y < rows-1 and horizontal_walls[y][x] == 1 and (x, y+1) not in visited:
            neighbors.append((x, y+1))
        if x > 0 and vertical_walls[y][x-1] == 1 and (x-1, y) not in visited:
            neighbors.append((x-1, y))
        if x < cols-1 and vertical_walls[y][x] == 1 and (x+1, y) not in visited:
            neighbors.append((x+1, y))

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)  # Добавляем соседа в очередь
                visited[neighbor] = current  # Отмечаем его как посещенного

    if goal not in visited:
        return []  # Путь невозможен, если цель не была достигнута

    # Восстановление пути от цели до старта
    path = []
    current = goal
    while current:
        path.append(current)
        current = visited[current]
    path.reverse()  # Разворачиваем путь
    return path  # Возвращаем путь

def save_maze_to_file(file_path, rows, cols, vertical_walls, horizontal_walls):
    # Сохранение лабиринта в файл
    with open(file_path, 'w') as f:
        f.write(f"{rows} {cols}\n")  # Запись размеров

        # Запись вертикальных стен
        for row in vertical_walls:
            f.write(" ".join(str(1 - v) for v in row) + "\n")

        f.write("\n")  # Пустая строка между секциями

        # Запись горизонтальных стен
        for row in horizontal_walls:
            f.write(" ".join(str(1 - h) for h in row) + "\n")
