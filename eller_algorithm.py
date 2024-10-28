import random

S, E = 1, 2  # Константы для юга (S) и востока (E)

class EllerMaze:
    def __init__(self, width, next_set=-1):
        self.width = width  # Ширина лабиринта
        self.next_set = next_set  # Индекс для следующего множества
        self.sets = {}  # Множества ячеек
        self.cells = {}  # Ячейки с их соответствующими множествами

    def next_state(self):
        # Создание нового состояния лабиринта
        return EllerMaze(self.width, self.next_set)

    def populate(self):
        # Заполнение ячеек лабиринта и распределение их по множествам
        for cell in range(self.width):
            if cell not in self.cells:
                self.next_set += 1
                # Добавляем новую ячейку в множество
                self.sets.setdefault(self.next_set, []).append(cell)
                self.cells[cell] = self.next_set  # Присваиваем ячейке множество
        return self

    def merge(self, sink_cell, target_cell):
        # Объединение двух ячеек в одно множество
        sink = self.cells[sink_cell]
        target = self.cells[target_cell]

        # Обновление множества и ячеек
        for cell in self.sets[target]:
            self.cells[cell] = sink
            self.sets[sink].append(cell)
        del self.sets[target]  # Удаляем целевое множество

    def same(self, cell1, cell2):
        # Проверка, принадлежат ли ячейки одному множеству
        return self.cells[cell1] == self.cells[cell2]

    def add(self, cell, set_id):
        # Добавление ячейки в указанное множество
        self.cells[cell] = set_id
        self.sets.setdefault(set_id, []).append(cell)
        return self

    def each_set(self):
        # Возвращает множества и их ячейки
        for set_id, cells in self.sets.items():
            yield set_id, cells


def step(state, finish=False):
    connected_sets = []  # Хранение соединенных множеств
    connected_set = [0]  # Первоначально одно множество

    # Создание горизонтальных соединений
    for c in range(state.width - 1):
        # Проверяем, нужно ли соединять текущие ячейки
        if state.same(c, c + 1) or (not finish and random.choice([True, False])):
            connected_sets.append(connected_set)  # Добавляем текущее множество
            connected_set = [c + 1]  # Начинаем новое множество
        else:
            state.merge(c, c + 1)  # Объединяем ячейки в одно множество
            connected_set.append(c + 1)

    connected_sets.append(connected_set)  # Добавляем последнее множество

    verticals = []  # Хранение вертикальных соединений
    next_state = state.next_state()

    if not finish:
        # Соединяем ячейки по вертикали случайным образом
        for set_id, cells in state.each_set():
            cells_to_connect = random.sample(cells, random.randint(1, len(cells)))
            verticals.extend(cells_to_connect)
            for cell in cells_to_connect:
                next_state.add(cell, set_id)
    else:
        # Завершаем лабиринт, соединяя ячейки с правым краем
        for set_id, cells in state.each_set():
            for cell in cells:
                if not state.same(cell, state.width - 1):
                    state.merge(cell, state.width - 1)

    row = []
    # Построение строки с горизонтальными и вертикальными стенами
    for connected_set in connected_sets:
        for i, cell in enumerate(connected_set):
            last = (i + 1 == len(connected_set))  # Проверяем, последняя ли ячейка
            map_value = 0 if last else E  # Добавляем стену на восток
            if cell in verticals:
                map_value |= S  # Добавляем стену на юг
            row.append(map_value)

    return next_state.populate(), row  # Возвращаем следующее состояние и строку


def generate_maze(width, height=None, seed=None):
    random.seed(seed)  # Устанавливаем зерно для случайных чисел
    state = EllerMaze(width).populate()  # Инициализация состояния лабиринта
    vertical_walls = []  # Вертикальные стены
    horizontal_walls = []  # Горизонтальные стены

    row_count = 0
    # Генерация строк лабиринта
    while height is None or row_count < height - 1:
        state, row = step(state)  # Переход к следующей строке
        vertical_walls.append([1 if cell & E else 0 for cell in row])  # Сохраняем вертикальные стены
        horizontal_walls.append([1 if cell & S else 0 for cell in row])  # Сохраняем горизонтальные стены
        row_count += 1

    state, row = step(state, finish=True)  # Последний шаг
    vertical_walls.append([1 if cell & E else 0 for cell in row])  # Последняя строка вертикальных стен
    horizontal_walls.append([0] * width)  # Последняя строка горизонтальных стен

    return vertical_walls, horizontal_walls  # Возвращаем стены
