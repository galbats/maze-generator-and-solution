# A1_Maze_Python

## Описание 

Этот проект реализует генерацию и решение лабиринтов с использованием различных алгоритмов. Также в проекте есть графический интерфейс и набор утилит для работы с файлами.

## Использование
- Генерация лабиринтов: Реализованы алгоритмы для генерации лабиринтов — Eller и алгоритм генерации пещер.
- Решение лабиринтов: Используется алгоритм BFS (поиск в ширину) для решения лабиринтов.
- Графический интерфейс: Интерфейс для интерактивной работы с лабиринтами.

## Структура проекта

```
.
├── Makefile                # Сценарий сборки и установки
├── cave_algorithm.py       # Алгоритм генерации пещер
├── eller_algorithm.py      # Алгоритм генерации лабиринта Эллера
├── file_utils.py           # Утилиты для работы с файлами лабиринтов
├── gui.py                  # Графический интерфейс для работы с лабиринтами
├── main.py                 # Основной файл для запуска проекта
├── mazes                   # Папка с примерами лабиринтов
│   ├── 1.txt               # Пример лабиринта 1
│   └── 2.txt               # Пример лабиринта 2
└── tests                   # Тесты для проверки функциональности
    ├── test_cave.py        # Тесты для алгоритма генерации пещер
    ├── test_eller.py       # Тесты для алгоритма Эллера
    └── test_solver.py      # Тесты для решения лабиринтов
```


## Запуск проекта

Установите необходимые зависимости в виртуальном окружении:

```
pip install -r requirements.txt
```

Выполните команду:

```
make
```

## Запуск тестов
Чтобы запустить тесты, используйте команду:

```
make tests
```

Тесты запускаются с помощью unittest, а также генерируется отчет о покрытии кода.
