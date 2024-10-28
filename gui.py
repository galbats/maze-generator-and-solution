from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.clock import Clock
from eller_algorithm import generate_maze  # Импорт функции для генерации лабиринта
from file_utils import load_maze_from_file, save_maze_to_file, bfs_solve  # Импорт функций для работы с файлами и алгоритмом поиска
from cave_algorithm import initialize_cave, update_cave, load_cave_from_file, save_cave_to_file  # Импорт функций для работы с пещерой

class MazeWidget(Widget):  
    # Виджет для отображения лабиринта
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 10  # Количество строк в лабиринте
        self.cols = 10  # Количество столбцов в лабиринте
        self.vertical_walls = None  # Вертикальные стены
        self.horizontal_walls = None  # Горизонтальные стены
        self.start = None  # Начальная точка для поиска пути
        self.end = None  # Конечная точка для поиска пути
        self.path = []  # Найденный путь
        self.cell_size = None  # Размер ячейки

    def on_touch_down(self, touch):  
        
        # Обработчик нажатий на экран
        if not self.cell_size:
            return  # Если размер ячейки не определён, ничего не делать

        x, y = touch.pos  # Получаем координаты касания
        j = int(x // self.cell_size)  # Рассчитываем индекс столбца
        i = int((self.height - y) // self.cell_size)  # Рассчитываем индекс строки

        # Проверяем, чтобы координаты были в пределах лабиринта
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return

        if not self.start:
            self.start = (j, i)  # Устанавливаем начальную точку
            print(f"Start point set at {self.start}")
        elif not self.end:
            self.end = (j, i)  # Устанавливаем конечную точку и запускаем поиск пути
            print(f"End point set at {self.end}")
            self.solve_maze()
        else:
            self.start = (j, i)  # Если обе точки заданы, сбрасываем конечную точку и путь
            self.end = None
            self.path = []
            print(f"New start point set at {self.start}")

        self.draw_maze(self.rows, self.cols, self.vertical_walls, self.horizontal_walls)  # Перерисовываем лабиринт

    def draw_maze(self, rows, cols, vertical_walls, horizontal_walls):  
        # Функция для отрисовки лабиринта
        self.canvas.clear()  # Очищаем холст
        with self.canvas:
            self.rows = rows
            self.cols = cols
            self.cell_size = min(self.width / cols, self.height / rows)  # Рассчитываем размер ячеек

            Rectangle(pos=self.pos, size=self.size, color=(1, 1, 1, 1))  # Заливаем фон

            Color(0, 0, 0, 1)  # Цвет линий (черный)

            # Отрисовка вертикальных и горизонтальных стен
            for i in range(rows):
                for j in range(cols):
                    x, y = j * self.cell_size, self.height - (i + 1) * self.cell_size

                    if vertical_walls[i][j] == 0:  # Если вертикальная стена отсутствует
                        Line(points=[x + self.cell_size, y, x + self.cell_size, y + self.cell_size], width=2)

                    if horizontal_walls[i][j] == 0:  # Если горизонтальная стена отсутствует
                        Line(points=[x, y, x + self.cell_size, y], width=2)

            # Отрисовка начальной точки
            if self.start:
                Color(0, 1, 0, 1)  # Цвет начальной точки (зелёный)
                x, y = self.start
                Line(circle=((x + 0.5) * self.cell_size, self.height - (y + 0.5) * self.cell_size, self.cell_size / 3), width=2)

            # Отрисовка конечной точки
            if self.end:
                Color(1, 0, 0, 1)  # Цвет конечной точки (красный)
                x, y = self.end
                Line(circle=((x + 0.5) * self.cell_size, self.height - (y + 0.5) * self.cell_size, self.cell_size / 3), width=2)

            # Отрисовка найденного пути
            if self.path:
                Color(1, 0, 0, 1)  # Цвет пути (красный)
                for idx in range(1, len(self.path)):
                    x1, y1 = self.path[idx - 1]
                    x2, y2 = self.path[idx]
                    Line(points=[
                        (x1 + 0.5) * self.cell_size, self.height - (y1 + 0.5) * self.cell_size,
                        (x2 + 0.5) * self.cell_size, self.height - (y2 + 0.5) * self.cell_size
                    ], width=2)

    def generate_and_draw(self, rows, cols):  
        # Генерация и отрисовка лабиринта
        self.vertical_walls, self.horizontal_walls = generate_maze(cols, rows)  # Генерация стен
        self.start = self.end = None  # Сброс начальной и конечной точки
        self.path = []  # Очистка пути
        self.draw_maze(rows, cols, self.vertical_walls, self.horizontal_walls)  # Отрисовка лабиринта

    def load_and_draw(self, file_path):  
        # Загрузка лабиринта из файла и его отрисовка
        rows, cols, vertical_walls, horizontal_walls = load_maze_from_file(file_path)
        self.rows = rows
        self.cols = cols
        self.vertical_walls = vertical_walls
        self.horizontal_walls = horizontal_walls
        self.start = self.end = None  # Сброс начальной и конечной точки
        self.path = []  # Очистка пути
        self.draw_maze(rows, cols, vertical_walls, horizontal_walls)  # Отрисовка лабиринта

    def solve_maze(self):  
        # Поиск пути в лабиринте
        if not self.start or not self.end:
            return  # Если не установлены начальная или конечная точки, завершить

        self.path = bfs_solve(self, self.start, self.end, self.vertical_walls, self.horizontal_walls)  # Поиск пути с помощью BFS
        if not self.path:
            print(f"Path from {self.start} to {self.end} not found.")  # Путь не найден
        else:
            print(f"Path found: {self.path}")  # Путь найден
        self.draw_maze(self.rows, self.cols, self.vertical_walls, self.horizontal_walls)  # Перерисовка лабиринта с путём

    def save_maze(self, file_name):  
        # Сохранение лабиринта в файл
        file_path = f"mazes/{file_name}.txt"  # Путь к файлу
        save_maze_to_file(file_path, self.rows, self.cols, self.vertical_walls, self.horizontal_walls)  # Сохранение данных лабиринта
        print(f"Maze saved to {file_path}")  # Сообщение об успешном сохранении

class CaveWidget(Widget):  
    # Виджет для отображения пещеры
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 10  # Количество строк в пещере
        self.cols = 10  # Количество столбцов в пещере
        self.cave = None  # Состояние пещеры
        self.birth_limit = 4  # Порог для рождения новой клетки
        self.death_limit = 3  # Порог для "смерти" клетки
        self.initial_chance = 0.45  # Начальная вероятность существования клетки
        self.running = False  # Флаг автоматического выполнения шагов
        self.step_delay = 1  # Задержка между шагами в автоматическом режиме (в секундах)

    def initialize_and_draw_cave(self):  
        # Инициализация и отрисовка пещеры
        self.cave = initialize_cave(self.rows, self.cols, self.initial_chance)  # Инициализация пещеры
        self.draw_cave()  # Отрисовка пещеры

    def draw_cave(self):  
        # Отрисовка пещеры
        self.canvas.clear()  # Очистка холста
        cell_size = min(self.width / self.cols, self.height / self.rows)  # Рассчет размера ячеек
        with self.canvas:
            for i in range(self.rows):
                for j in range(self.cols):
                    x = j * cell_size
                    y = self.height - (i + 1) * cell_size
                    if self.cave[i][j] == 1:
                        Color(0, 0, 0, 1)  # Черный для "живых" клеток
                    else:
                        Color(1, 1, 1, 1)  # Белый для "мёртвых" клеток
                    Rectangle(pos=(x, y), size=(cell_size, cell_size))  # Отрисовка ячеек

    def step_cave(self):  
        # Один шаг клеточного автомата
        self.cave = update_cave(self.cave, self.birth_limit, self.death_limit)  # Обновление состояния пещеры
        self.draw_cave()  # Перерисовка пещеры

    def auto_step(self, dt):  
        # Автоматическое выполнение шагов
        if self.running:
            self.step_cave()  # Выполняем шаг, если автоматический режим включен

    def toggle_auto_run(self, state):  
        # Включение/выключение автоматической генерации
        if state == 'down':
            self.running = True  # Включаем автоматический режим
            Clock.schedule_interval(self.auto_step, self.step_delay)  # Запускаем таймер с задержкой между шагами
        else:
            self.running = False  # Выключаем автоматический режим
            Clock.unschedule(self.auto_step)  # Останавливаем таймер

    def load_and_draw_cave(self, file_path):  
        # Загрузка и отрисовка пещеры из файла
        self.rows, self.cols, self.cave = load_cave_from_file(file_path)  # Загрузка состояния пещеры
        self.draw_cave()  # Отрисовка пещеры

    def save_cave(self, file_name):  
        # Сохранение пещеры в файл
        save_cave_to_file(f"mazes/{file_name}.txt", self.cave)  # Сохранение текущего состояния пещеры
