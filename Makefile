# Имя проекта
PROJECT_NAME = my_maze_project

# Каталог установки — папка build в текущей директории
PREFIX = build

# Файлы проекта
SRC_FILES = cave_algorithm.py eller_algorithm.py file_utils.py gui.py main.py
TEST_FILES = tests/test_cave.py tests/test_eller.py tests/test_solver.py

# Цель по умолчанию
all: $(SRC_FILES)
	@echo "Сборка завершена"
	python main.py    

# Установка программы в папку build
install: $(SRC_FILES)
	@echo "Установка программы в $(PREFIX)"
	mkdir -p $(PREFIX)
	cp $(SRC_FILES) $(PREFIX)/
	@echo "Программа установлена в $(PREFIX)"

# Удаление программы из папки build
uninstall:
	@echo "Удаление программы из $(PREFIX)"
	rm -f $(PREFIX)/cave_algorithm.py
	rm -f $(PREFIX)/eller_algorithm.py
	rm -f $(PREFIX)/file_utils.py
	rm -f $(PREFIX)/gui.py
	rm -f $(PREFIX)/main.py
	rmdir $(PREFIX)
	@echo "Программа удалена из $(PREFIX)"

# Очистка проекта от скомпилированных файлов, временных файлов и файлов тестов
clean:
	@echo "Очистка проекта"
	rm -rf *.pyc __pycache__ */__pycache__
	rm -rf build
	rm -rf *.log
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf dist
	@echo "Проект очищен"

# Создание архива проекта
dist:
	@echo "Создание архива проекта"
	mkdir -p dist
	cp -r $(SRC_FILES) mazes dist/
	tar -czvf $(PROJECT_NAME).tar.gz dist
	@echo "Архив проекта $(PROJECT_NAME).tar.gz создан"

# Запуск тестов
tests:
	@echo "Запуск тестов"
	coverage run -m unittest discover -s tests
	coverage report
	@echo "Тесты завершены"

.PHONY: all install uninstall clean dvi dist tests
