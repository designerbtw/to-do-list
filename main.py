import sqlite3
import time
import sys
from tkinter import dialog
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QSpinBox, QPushButton, QMessageBox, QListWidgetItem)
from PyQt5.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from ui_dialog import Ui_Dialog

class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
        self.timestamp = int(time.time())

    def __str__(self):
        return f"Задача: {self.title}, Описание: {self.description}, Приоритет: {self.priority}, Время добавления: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.timestamp))}"


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
        print(f"Задача '{task.title}' добавлена.")

    def view_tasks(self):
        query = "SELECT * FROM tasks ORDER BY timestamp DESC"
        self.cursor.execute(query)
        tasks = self.cursor.fetchall()
        if tasks:
            for task in tasks:
                # task[0] - id, task[1] - title, task[2] - description, task[3] - priority, task[4] - timestamp
                task_obj = Task(task[1], task[2], task[3])
                task_obj.timestamp = task[4]
                print(f"ID: {task[0]} | {task_obj}")
        else:
            print("Задачи не найдены.")

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.cursor.execute(query, (task_id,))
        self.conn.commit()
        print(f"Задача с ID {task_id} удалена.")

    def update_task(self, task_id, title=None, description=None, priority=None):
        query = "SELECT * FROM tasks WHERE id = ?"
        self.cursor.execute(query, (task_id,))
        task = self.cursor.fetchone()
        if task:
            new_title = title if title else task[1]
            new_description = description if description else task[2]
            new_priority = priority if priority is not None else task[3]
            query = """
            UPDATE tasks
            SET title = ?, description = ?, priority = ?
            WHERE id = ?
            """
            self.cursor.execute(query, (new_title, new_description, new_priority, task_id))
            self.conn.commit()
            print(f"Задача с ID {task_id} обновлена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def close(self):
        self.conn.close()

class add_task_dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.priority_box.addItems([str(i) for i in range(1, 6)])
        self.apply_button.clicked.connect(self.accept)

    def get_task_data(self):
        title = self.task_name.text()
        description = self.task_desc.text()
        priority = int(self.priority_box.currentText())
        return title, description, priority

class ToDoApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.todo_list = ToDoList()
        self.load_tasks()

        self.pushButton.clicked.connect(self.open_add_dialog)
        self.delete_task.clicked.connect(self.delete_selected_task)
        self.update_all.clicked.connect(self.load_tasks)

    def load_tasks(self):
        self.listWidget.clear()
        query = "SELECT * FROM tasks ORDER BY timestamp DESC"
        self.todo_list.cursor.execute(query)
        tasks = self.todo_list.cursor.fetchall()
        for task in tasks:
            item = QListWidgetItem(f"ID: {task[0]} | {task[1]} (Приоритет: {task[3]})")
            item.setData(Qt.UserRole, task[0])
            self.listWidget.addItem(item)

    def open_add_dialog(self):
        dialog = add_task_dialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description, priority = dialog.get_task_data()
            new_task = Task(title, description, priority)
            self.todo_list.add_task(new_task)
            self.load_tasks()

    def delete_selected_task(self):
        selected_item = self.listWidget.currentItem()
        if selected_item:
            task_id = selected_item.data(Qt.UserRole)
            self.todo_list.delete_task(task_id)
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите задачу для удаления.")

    def closeEvent(self, event):
        self.todo_list.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())

    task1 = Task("Купить продукты", "Купить молоко, хлеб и овощи", 2)
    task2 = Task("Закончить проект", "Завершить работу над проектом", 1)

    todo.add_task(task1)
    todo.add_task(task2)

    print("\nВсе задачи:")
    todo.view_tasks()

    todo.delete_task(1)

    print("\nПосле удаления задачи с ID 1:")
    todo.view_tasks()

    todo.close()
