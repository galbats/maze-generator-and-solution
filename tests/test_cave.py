import unittest
from cave_algorithm import initialize_cave, count_alive_neighbors, update_cave, load_cave_from_file, save_cave_to_file
import os

class TestCaveAlgorithm(unittest.TestCase):

    def test_initialize_cave(self):
        # Тестирует функцию initialize_cave, которая инициализирует пещеру
        rows, cols, initial_chance = 5, 5, 0.5
        cave = initialize_cave(rows, cols, initial_chance)
        self.assertEqual(len(cave), rows, "Должно быть правильное количество строк")
        self.assertEqual(len(cave[0]), cols, "Должно быть правильное количество столбцов")
        # Проверим, что значения в пещере либо 0, либо 1
        for row in cave:
            for cell in row:
                self.assertIn(cell, [0, 1], "Клетка должна быть либо живой (1), либо мертвой (0)")
    
    def test_count_alive_neighbors(self):
        # Тестируем пещеру размером 3x3
        cave = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ]
        rows, cols = 3, 3

        # Тестируем ячейку в углу (0, 0)
        # Ожидаем 8, так как 5 из 8 соседей за пределами пещеры, которые считаются "живыми"
        self.assertEqual(count_alive_neighbors(cave, 0, 0, rows, cols), 8, "Количество живых соседей должно быть 8")

        # Тестируем центральную ячейку (1, 1)
        # Ожидаем 3, так как вокруг нее 3 живых клетки
        self.assertEqual(count_alive_neighbors(cave, 1, 1, rows, cols), 3, "Количество живых соседей должно быть 3")

        # Тестируем ячейку на краю (2, 2)
        # Ожидаем 6, так как 3 из 8 соседей за пределами пещеры, которые считаются "живыми"
        self.assertEqual(count_alive_neighbors(cave, 2, 2, rows, cols), 6, "Количество живых соседей должно быть 6")

    def test_update_cave(self):
        # Тестирует функцию update_cave, которая обновляет состояние пещеры
        cave = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ]
        birth_limit = 3
        death_limit = 2
        new_cave = update_cave(cave, birth_limit, death_limit)
        expected_cave = [
            [1, 1, 1],  # Ожидание обновления по правилам рождения и смерти
            [1, 1, 1],
            [1, 1, 1]
        ]
        self.assertEqual(new_cave, expected_cave, "Состояние пещеры должно обновиться правильно")

    def test_load_cave_from_file(self):
        # Тестирует функцию load_cave_from_file, которая загружает пещеру из файла
        file_path = "test_cave.txt"
        with open(file_path, 'w') as f:
            f.write("3 3\n")
            f.write("0 1 0\n")
            f.write("1 1 0\n")
            f.write("0 0 1\n")
        
        rows, cols, cave = load_cave_from_file(file_path)
        self.assertEqual(rows, 3, "Количество строк должно быть 3")
        self.assertEqual(cols, 3, "Количество столбцов должно быть 3")
        expected_cave = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ]
        self.assertEqual(cave, expected_cave, "Загруженная пещера должна быть правильной")
        os.remove(file_path)  # Удаляем временный файл после теста

    def test_save_cave_to_file(self):
        # Тестирует функцию save_cave_to_file, которая сохраняет пещеру в файл
        file_path = "test_output_cave.txt"
        cave = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ]
        save_cave_to_file(file_path, cave)
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        expected_content = "3 3\n0 1 0\n1 1 0\n0 0 1\n"
        self.assertEqual(content, expected_content, "Содержимое файла должно соответствовать сохраненной пещере")
        os.remove(file_path)  # Удаляем временный файл после теста

if __name__ == "__main__":
    unittest.main()
