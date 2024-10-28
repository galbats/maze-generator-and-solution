from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import os
from gui import MazeWidget, CaveWidget

class MazeApp(App):
    def build(self):
        # Основная структура приложения с вкладками
        panel = TabbedPanel()
        panel.do_default_tab = False  # Отключаем дефолтную вкладку

        # Вкладки для лабиринтов и пещер
        maze_layout = self.build_maze_tab()
        cave_layout = self.build_cave_tab()

        # Добавляем вкладки
        panel.add_widget(maze_layout)
        panel.add_widget(cave_layout)

        return panel

    def build_maze_tab(self):
        # Создаем вкладку для лабиринта
        maze_tab = TabbedPanelItem(text="Maze")
        layout = BoxLayout(orientation='vertical')
        self.maze_widget = MazeWidget(size_hint=(1, 0.8))  # Создаем виджет для лабиринта

        # Добавляем элементы управления для лабиринта
        control_layout = BoxLayout(size_hint=(1, 0.2))

        self.rows_input = TextInput(text='10', multiline=False, input_filter='int', hint_text="Rows")  # Поле ввода для строк
        self.cols_input = TextInput(text='10', multiline=False, input_filter='int', hint_text="Cols")  # Поле ввода для столбцов

        generate_btn = Button(text="Generate", on_press=self.on_generate)  # Кнопка для генерации лабиринта
        load_btn = Button(text="Load", on_press=self.on_load)  # Кнопка для загрузки лабиринта
        save_btn = Button(text="Save", on_press=self.on_save)  # Кнопка для сохранения лабиринта

        control_layout.add_widget(Label(text="Rows:"))  # Метка для поля ввода строк
        control_layout.add_widget(self.rows_input)
        control_layout.add_widget(Label(text="Cols:"))  # Метка для поля ввода столбцов
        control_layout.add_widget(self.cols_input)
        control_layout.add_widget(generate_btn)
        control_layout.add_widget(load_btn)
        control_layout.add_widget(save_btn)

        layout.add_widget(control_layout)
        layout.add_widget(self.maze_widget)

        maze_tab.add_widget(layout)
        return maze_tab

    def build_cave_tab(self):
        # Создаем вкладку для пещеры
        cave_tab = TabbedPanelItem(text="Cave")
        layout = BoxLayout(orientation='vertical')
        self.cave_widget = CaveWidget(size_hint=(1, 0.8))  # Создаем виджет для пещеры

        # Добавляем элементы управления для пещеры
        control_layout = BoxLayout(size_hint=(1, 0.2))

        self.rows_input_cave = TextInput(text='10', multiline=False, input_filter='int', hint_text="Rows (max 50)")  # Поле ввода для строк
        self.cols_input_cave = TextInput(text='10', multiline=False, input_filter='int', hint_text="Cols (max 50)")  # Поле ввода для столбцов
        self.birth_input = TextInput(text='4', multiline=False, input_filter='int', hint_text="Birth limit")  # Поле ввода для порога рождения
        self.death_input = TextInput(text='3', multiline=False, input_filter='int', hint_text="Death limit")  # Поле ввода для порога смерти
        self.init_chance_input = TextInput(text='0.45', multiline=False, input_filter='float', hint_text="Initial chance")  # Поле ввода для начальной вероятности

        initialize_btn = Button(text="Initialize", on_press=self.on_initialize_cave)  # Кнопка для инициализации пещеры
        step_btn = Button(text="Step", on_press=self.on_step_cave)  # Кнопка для выполнения одного шага
        self.auto_btn = Button(text="Auto", on_press=self.on_auto_cave)  # Кнопка для автоматического режима

        control_layout.add_widget(Label(text="Rows:"))
        control_layout.add_widget(self.rows_input_cave)
        control_layout.add_widget(Label(text="Cols:"))
        control_layout.add_widget(self.cols_input_cave)
        control_layout.add_widget(Label(text="Birth\nLimit:"))
        control_layout.add_widget(self.birth_input)
        control_layout.add_widget(Label(text="Death\nLimit:"))
        control_layout.add_widget(self.death_input)
        control_layout.add_widget(Label(text="Init\nChance:"))
        control_layout.add_widget(self.init_chance_input)
        control_layout.add_widget(initialize_btn)
        control_layout.add_widget(step_btn)
        control_layout.add_widget(self.auto_btn)

        layout.add_widget(control_layout)
        layout.add_widget(self.cave_widget)

        cave_tab.add_widget(layout)
        return cave_tab

    def on_generate(self, instance):
        # Обработчик нажатия кнопки генерации лабиринта
        try:
            rows = int(self.rows_input.text)
            cols = int(self.cols_input.text)
            if rows > 0 and cols > 0:
                self.maze_widget.generate_and_draw(rows, cols)  # Генерация и отрисовка лабиринта
            else:
                self.show_error("Rows and Cols must be positive integers.")  # Ошибка ввода
        except ValueError:
            self.show_error("Invalid input for Rows and Cols.")  # Ошибка преобразования

    def on_load(self, instance):
        # Обработчик нажатия кнопки загрузки лабиринта
        self.show_file_chooser()  # Показываем диалог выбора файла

    def on_save(self, instance):
        # Обработчик нажатия кнопки сохранения лабиринта
        file_name = "generated_maze"  # Имя файла для сохранения
        self.maze_widget.save_maze(file_name)  # Сохраняем лабиринт

    def on_initialize_cave(self, instance):
        # Обработчик нажатия кнопки инициализации пещеры
        try:
            rows = int(self.rows_input_cave.text)
            cols = int(self.cols_input_cave.text)
            if rows > 50 or cols > 50:
                self.show_error("Maximum size for Rows and Cols is 50.")  # Ошибка ввода
                return

            birth_limit = int(self.birth_input.text)
            death_limit = int(self.death_input.text)
            init_chance = float(self.init_chance_input.text)

            self.cave_widget.rows = rows
            self.cave_widget.cols = cols
            self.cave_widget.birth_limit = birth_limit
            self.cave_widget.death_limit = death_limit
            self.cave_widget.initial_chance = init_chance
            self.cave_widget.initialize_and_draw_cave()  # Инициализируем и отрисовываем пещеру
        except ValueError:
            self.show_error("Invalid input for Cave parameters.")  # Ошибка ввода

    def on_step_cave(self, instance):
        # Обработчик нажатия кнопки выполнения шага
        self.cave_widget.step_cave()  # Выполняем один шаг в пещере

    def on_auto_cave(self, instance):
        # Обработчик нажатия кнопки автоматического режима
        if self.auto_btn.text == "Auto":
            self.cave_widget.toggle_auto_run('down')  # Включаем автоматический режим
            self.auto_btn.text = "Stop\nAuto"  # Изменяем текст кнопки
        else:
            self.cave_widget.toggle_auto_run('normal')  # Выключаем автоматический режим
            self.auto_btn.text = "Auto"  # Изменяем текст кнопки

    def show_file_chooser(self):
        # Отображение диалога выбора файла
        current_directory = os.getcwd()  # Текущая рабочая директория
        content = FileChooserListView(path=current_directory)  # Виджет выбора файла
        popup = Popup(title='Load Maze', content=content, size_hint=(0.9, 0.9))  # Создаем всплывающее окно

        def on_file_select(chooser, selection):
            if selection:
                try:
                    file_path = selection[0]  # Путь к выбранному файлу
                    self.maze_widget.load_and_draw(file_path)  # Загружаем и отрисовываем лабиринт
                    popup.dismiss()  # Закрываем всплывающее окно
                except Exception as e:
                    self.show_error(f"Failed to load maze: {e}")  # Ошибка загрузки лабиринта

        content.bind(on_submit=lambda instance, selection, _: on_file_select(instance, selection))  # Обработка выбора файла
        popup.open()  # Открываем всплывающее окно

    def show_error(self, message):
        # Отображение сообщения об ошибке
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.5, 0.5))  # Создаем всплывающее окно с ошибкой
        popup.open()  # Открываем всплывающее окно


if __name__ == "__main__":
    MazeApp().run()  # Запускаем приложение
