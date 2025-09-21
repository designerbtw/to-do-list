import sys
import sqlite3
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, QListWidget, QInputDialog

class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
        self.timestamp = int(time.time())  # время добавления задачи в Unix-формате

    def __str__(self):
        return f"Задача: {self.title} | {self.description} | Приоритет: {self.priority}"

class ToDoList:
    def __init__(self, db_name="todo_list.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER,
            timestamp INTEGER
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_task(self, task):
        query = "INSERT INTO tasks (title, description, priority, timestamp) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (task.title, task.description, task.priority, task.timestamp))
        self.conn.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.cursor.execute(query, (task_id,))
        self.conn.commit()

    def get_all_tasks(self):
        query = "SELECT * FROM tasks ORDER BY timestamp DESC"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_status(self, task_id, status):
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.cursor.execute(query, (status, task_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 600, 400)

        self.todo_list = ToDoList()

        self.init_ui()

    def init_ui(self):
        # Основной макет
        main_layout = QVBoxLayout()

        # Виджеты для добавления задачи
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Введите название задачи")
        self.desc_input = QLineEdit(self)
        self.desc_input.setPlaceholderText("Введите описание задачи")
        self.priority_combobox = QComboBox(self)
        self.priority_combobox.addItems(["1 - Высокий", "2 - Средний", "3 - Низкий"])

        self.add_button = QPushButton("Добавить задачу", self)
        self.add_button.clicked.connect(self.add_task)

        # Виджет для отображения списка задач
        self.task_list_widget = QListWidget(self)

        # Кнопка для удаления задачи
        self.delete_button = QPushButton("Удалить задачу", self)
        self.delete_button.clicked.connect(self.delete_task)

        # Кнопка для обновления статуса
        self.update_button = QPushButton("Обновить статус", self)
        self.update_button.clicked.connect(self.update_task_status)

        # Кнопка для обновления списка задач
        self.refresh_button = QPushButton("Обновить список задач", self)
        self.refresh_button.clicked.connect(self.refresh_task_list)

        # Добавление виджетов на основной макет
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.desc_input)
        input_layout.addWidget(self.priority_combobox)
        input_layout.addWidget(self.add_button)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_list_widget)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.update_button)
        main_layout.addWidget(self.refresh_button)

        self.setLayout(main_layout)

        # Инициализация списка задач
        self.refresh_task_list()

    def add_task(self):
        title = self.title_input.text()
        description = self.desc_input.text()
        priority = self.priority_combobox.currentIndex() + 1  # Преобразуем индекс в приоритет

        if title and description:
            task = Task(title, description, priority)
            self.todo_list.add_task(task)
            self.refresh_task_list()
            self.title_input.clear()
            self.desc_input.clear()

    def delete_task(self):
        task_id = self.get_task_id_from_list()
        if task_id:
            self.todo_list.delete_task(task_id)
            self.refresh_task_list()

    def update_task_status(self):
        task_id = self.get_task_id_from_list()
        if task_id:
            status, ok = QInputDialog.getItem(self, "Обновить статус", "Выберите статус:", ["Не выполнено", "Выполнено"], 0, False)
            if ok:
                self.todo_list.update_status(task_id, status)
                self.refresh_task_list()

    def get_task_id_from_list(self):
        selected_item = self.task_list_widget.currentItem()
        if selected_item:
            task_info = selected_item.text()
            task_id = int(task_info.split('|')[0].split(':')[1].strip())
            return task_id
        return None

    def refresh_task_list(self):
        self.task_list_widget.clear()
        tasks = self.todo_list.get_all_tasks()
        for task in tasks:
            task_info = f"ID: {task[0]} | {task[1]} | {task[2]} | Приоритет: {task[3]}"
            self.task_list_widget.addItem(task_info)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
