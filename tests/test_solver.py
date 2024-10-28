import unittest
from file_utils import bfs_solve

class TestMazeSolver(unittest.TestCase):
    def setUp(self):
        # Настраиваем стены: 1 = стена, 0 = путь
        self.vertical_walls = [
            [1, 0, 1],  # Стены между (0,1) и (0,2), проход между (0,0) и (0,1)
            [1, 0, 0],  # Стены между (1,0) и (1,1), проход между (1,1) и (1,2)
            [1, 1, 1]   # Везде стены
        ]

        self.horizontal_walls = [
            [1, 1, 1],  # Верхняя стена полностью блокирована
            [0, 0, 1],  # Проход между (1,0) и (1,1), стена справа от (1,2)
            [1, 1, 1]   # Нижняя стена полностью блокирована
        ]

    def test_bfs_solve_no_path(self):
        # Тестирует случай, когда пути нет (цель окружена стенами)
        start = (0, 0)
        goal = (1, 2)  # Клетка окружена стенами
        expected_path = []
        path = bfs_solve(None, start, goal, self.vertical_walls, self.horizontal_walls)
        self.assertEqual(path, expected_path, "Путь не должен существовать")

    def test_bfs_solve_start_is_goal(self):
        # Тестирует случай, когда стартовая клетка совпадает с целью
        start = (0, 0)
        goal = (0, 0)
        expected_path = [(0, 0)]
        path = bfs_solve(None, start, goal, self.vertical_walls, self.horizontal_walls)
        self.assertEqual(path, expected_path, "Путь должен содержать только стартовую клетку")

if __name__ == "__main__":
    unittest.main()
