import unittest
from eller_algorithm import EllerMaze, step, generate_maze

class TestEllerAlgorithm(unittest.TestCase):
    def setUp(self):
        # Настройка перед тестами - создаем лабиринт с заданной шириной
        self.maze_width = 5
        self.eller_maze = EllerMaze(self.maze_width)

    def test_populate(self):
        # Тестирует функцию populate, которая инициализирует ячейки и множества
        maze = self.eller_maze.populate()
        self.assertEqual(len(maze.cells), self.maze_width, "Cells should be populated correctly")
        self.assertEqual(len(maze.sets), self.maze_width, "Sets should be created for each cell")

    def test_merge(self):
        # Тестирует функцию merge, которая объединяет два множества ячеек
        maze = self.eller_maze.populate()
        maze.merge(0, 1)
        self.assertTrue(maze.same(0, 1), "Cells 0 and 1 should be in the same set after merging")
        self.assertEqual(len(maze.sets), self.maze_width - 1, "Number of sets should decrease after merging")

    def test_same(self):
        # Тестирует функцию same, которая проверяет, принадлежат ли две ячейки одному множеству
        maze = self.eller_maze.populate()
        maze.merge(0, 1)
        self.assertTrue(maze.same(0, 1), "Cells 0 and 1 should be the same")
        self.assertFalse(maze.same(0, 2), "Cells 0 and 2 should not be the same")

    def test_add(self):
        # Тестирует функцию add, которая добавляет ячейку в конкретное множество
        maze = EllerMaze(3)
        maze.add(0, 0)
        self.assertEqual(maze.cells[0], 0, "Cell should be added with correct set id")
        self.assertIn(0, maze.sets[0], "Cell should be in the corresponding set")

    def test_each_set(self):
        # Тестирует функцию each_set, которая возвращает итератор по всем множествам
        maze = EllerMaze(3)
        maze.add(0, 0)
        sets = list(maze.each_set())
        self.assertEqual(len(sets), 1, "There should be only one set")
        self.assertEqual(sets[0][0], 0, "Set ID should be correct")
        self.assertEqual(sets[0][1], [0], "Cells in the set should be correct")

    def test_step(self):
        # Тестирует функцию step, которая выполняет один шаг алгоритма Эллера
        maze = EllerMaze(self.maze_width).populate()
        next_state, row = step(maze)
        self.assertEqual(len(row), self.maze_width, "Row should have the correct number of cells")
        self.assertIsInstance(next_state, EllerMaze, "Next state should be an instance of EllerMaze")

    def test_generate_maze(self):
        # Тестирует функцию generate_maze, которая генерирует полный лабиринт
        vertical_walls, horizontal_walls = generate_maze(self.maze_width, height=3, seed=42)
        self.assertEqual(len(vertical_walls), 3, "Vertical walls should be generated for each row")
        self.assertEqual(len(horizontal_walls), 3, "Horizontal walls should be generated for each row")
        self.assertEqual(len(vertical_walls[0]), self.maze_width, "Each row of vertical walls should match maze width")

if __name__ == "__main__":
    unittest.main()
