import sqlite3
import time
import sys
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, 
                             QPushButton, QMessageBox, QListWidgetItem)
from PyQt5.QtCore import Qt
from ui_mainwindow_new import Ui_MainWindow
from ui_dialog import Ui_Dialog
from ui_change_dialog import Ui_Dialog as Ui_ChangeDialog
from ui_login_dialog import Ui_LoginDialog
from ui_task_details_dialog import Ui_TaskDetailsDialog


class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
        self.timestamp = int(time.time())


class ToDoList:
    def __init__(self, db_name="todo_list.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        users_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at INTEGER
        );
        """
        self.cursor.execute(users_query)
        
        tasks_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER,
            timestamp INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        self.cursor.execute(tasks_query)        
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        password_hash = self.hash_password(password)
        timestamp = int(time.time())
        
        try:
            query = "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)"
            self.cursor.execute(query, (username, password_hash, timestamp))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, username, password):
        password_hash = self.hash_password(password)
        query = "SELECT id FROM users WHERE username = ? AND password_hash = ?"
        self.cursor.execute(query, (username, password_hash))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_task(self, task, user_id):
        query = "INSERT INTO tasks (user_id, title, description, priority, timestamp) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (user_id, task.title, task.description, task.priority, task.timestamp))
        self.conn.commit()

    def get_tasks(self, user_id=None):
        if user_id:
            query = 'SELECT * FROM tasks WHERE user_id = ? ORDER BY timestamp DESC'
            self.cursor.execute(query, (user_id,))
        else:
            query = 'SELECT * FROM tasks ORDER BY timestamp DESC'
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_task_by_id(self, task_id, user_id=None):
        if user_id:
            query = "SELECT * FROM tasks WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, (task_id, user_id))
        else:
            query = "SELECT * FROM tasks WHERE id = ?"
            self.cursor.execute(query, (task_id,))
        return self.cursor.fetchone()

    def delete_task(self, task_id, user_id=None):
        if user_id:
            query = "DELETE FROM tasks WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, (task_id, user_id))
        else:
            query = "DELETE FROM tasks WHERE id = ?"
            self.cursor.execute(query, (task_id,))
        self.conn.commit()

    def update_task(self, task_id, user_id=None, title=None, description=None, priority=None):
        if user_id:
            query = "SELECT * FROM tasks WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, (task_id, user_id))
        else:
            query = "SELECT * FROM tasks WHERE id = ?"
            self.cursor.execute(query, (task_id,))
        
        task = self.cursor.fetchone()
        if task:
            # структура базы данных: id, user_id, title, description, priority, timestamp
            new_title = title if title else task[2]
            new_description = description if description else task[3]
            new_priority = priority if priority is not None else task[4]
            
            if user_id:
                query = """
                UPDATE tasks SET title = ?, description = ?, priority = ?
                WHERE id = ? AND user_id = ?
                """
                self.cursor.execute(query, (new_title, new_description, new_priority, task_id, user_id))
            else:
                query = """
                UPDATE tasks SET title = ?, description = ?, priority = ?
                WHERE id = ?
                """
                self.cursor.execute(query, (new_title, new_description, new_priority, task_id))
            
            self.conn.commit()
        
    def close(self):
        self.conn.close()


class AddTaskDialog(QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.priority_box.addItems([str(i) for i in range(1, 6)])
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_task_data(self):
        title = self.task_name.text()
        description = self.task_desc.toPlainText()
        priority = int(self.priority_box.currentText())
        return title, description, priority


class ChangeTaskDialog(QDialog, Ui_ChangeDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.apply_change.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_task_data(self):
        title = self.lineEdit.text()
        description = self.textEdit.toPlainText()
        return title, description


class LoginDialog(QDialog, Ui_LoginDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.login_button.clicked.connect(self.login_clicked)
        self.register_button.clicked.connect(self.register_clicked)
        self.cancel_button.clicked.connect(self.reject)
        
        self.action = None
        
    def login_clicked(self):
        self.action = 'login'
        self.accept()
        
    def register_clicked(self):
        self.action = 'register'
        self.accept()
    
    def get_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        return username, password, self.action


class TaskDetailsDialog(QDialog, Ui_TaskDetailsDialog):
    
    def __init__(self, task_data, todo_list, user_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.task_data = task_data
        self.todo_list = todo_list
        self.user_id = user_id
        
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.close_button.clicked.connect(self.accept)
        
        self.populate_data()
    
    def populate_data(self):
        # структура базы данных: id, user_id, title, description, priority, timestamp
        task_id = self.task_data[0]
        title = self.task_data[2]
        description = self.task_data[3] or ""
        priority = self.task_data[4]
        timestamp = self.task_data[5]
        
        created_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
        
        self.id_value.setText(str(task_id))
        self.title_value.setText(title)
        self.description_value.setPlainText(str(description))
        self.priority_value.setText(str(priority))
        self.created_value.setText(created_date)
    
    def edit_task(self):
        dialog = ChangeTaskDialog(self)
        dialog.lineEdit.setText(self.task_data[2])
        dialog.textEdit.setPlainText(str(self.task_data[3] or ""))
        
        if dialog.exec_() == QDialog.Accepted:
            title, description = dialog.get_task_data()
            self.todo_list.update_task(self.task_data[0], self.user_id, title=title, description=description)
            
            self.task_data = list(self.task_data)
            self.task_data[2] = title
            self.task_data[3] = description
            self.populate_data()
            
            QMessageBox.information(self, "Успех", "Задача обновлена!")
    
    def delete_task(self):
        reply = QMessageBox.question(self, "Подтверждение", 
                                   "Вы уверены, что хотите удалить эту задачу?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.todo_list.delete_task(self.task_data[0], self.user_id)
            QMessageBox.information(self, "Успех", "Задача удалена!")
            self.accept()


class ToDoApp(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.todo_list = ToDoList()
        self.current_user_id = None
        self.current_username = None
        
        if self.show_login_dialog():
            self.setup_ui()
            self.load_tasks()
        else:
            sys.exit()
    
    def show_login_dialog(self):
        while True:
            dialog = LoginDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                username, password, action = dialog.get_credentials()
                
                if not username or not password:
                    QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
                    continue
                
                if action == 'login':
                    user_id = self.todo_list.authenticate_user(username, password)
                    if user_id:
                        self.current_user_id = user_id
                        self.current_username = username
                        QMessageBox.information(self, "Успех", f"Добро пожаловать, {username}!")
                        return True
                    else:
                        QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
                        
                elif action == 'register':
                    if self.todo_list.register_user(username, password):
                        QMessageBox.information(self, "Успех", 
                                              "Пользователь зарегистрирован! Теперь войдите в систему.")
                    else:
                        QMessageBox.warning(self, "Ошибка", 
                                          "Пользователь с таким именем уже существует!")
                        
            else:
                return False
    
    def setup_ui(self):
        self.setWindowTitle(f"Todo List - {self.current_username}")
        
        self.pushButton.clicked.connect(self.open_add_dialog)
        self.update_all.clicked.connect(self.load_tasks)
        
        self.listWidget.itemDoubleClicked.connect(self.on_item_double_clicked)

    def load_tasks(self):
        self.listWidget.clear()
        tasks = self.todo_list.get_tasks(self.current_user_id)
        for task in tasks:
            # Database structure: id, user_id, title, description, priority, timestamp
            item = QListWidgetItem(f"ID: {task[0]} | {task[2]} (Приоритет: {task[4]})")
            item.setData(Qt.UserRole, task[0])
            self.listWidget.addItem(item)
    
    def on_item_double_clicked(self, item):
        task_id = item.data(Qt.UserRole)
        task_data = self.todo_list.get_task_by_id(task_id, self.current_user_id)
        
        if task_data:
            dialog = TaskDetailsDialog(task_data, self.todo_list, self.current_user_id, self)
            if dialog.exec_() == QDialog.Accepted:
                self.load_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Задача не найдена!")

    def open_add_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description, priority = dialog.get_task_data()
            if title.strip():  # Only add if title is not empty
                new_task = Task(title, description, priority)
                self.todo_list.add_task(new_task, self.current_user_id)
                self.load_tasks()
            else:
                QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")

    def closeEvent(self, event):
        self.todo_list.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
