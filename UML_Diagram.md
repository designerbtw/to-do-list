# UML Диаграмма классов - ToDo List Application

```mermaid
classDiagram
    %% Основные классы
    class Task {
        -title: str
        -description: str
        -priority: int
        -timestamp: int
        +__init__(title, description, priority)
    }

    class ToDoList {
        -db_name: str
        -conn: sqlite3.Connection
        -cursor: sqlite3.Cursor
        +__init__(db_name)
        -_create_tables()
        +hash_password(password): str
        +register_user(username, password): bool
        +authenticate_user(username, password): int
        +add_task(task, user_id)
        +get_tasks(user_id): list
        +get_task_by_id(task_id, user_id): tuple
        +delete_task(task_id, user_id)
        +update_task(task_id, user_id, title, description, priority)
        +close()
    }

    %% GUI Классы - Диалоги
    class AddTaskDialog {
        +setupUi(self)
        +get_task_data(): tuple
    }

    class ChangeTaskDialog {
        +setupUi(self)
        +get_task_data(): tuple
    }

    class LoginDialog {
        -action: str
        +setupUi(self)
        +login_clicked()
        +register_clicked()
        +get_credentials(): tuple
    }

    class TaskDetailsDialog {
        -task_data: tuple
        -todo_list: ToDoList
        -user_id: int
        +setupUi(self)
        +populate_data()
        +edit_task()
        +delete_task()
    }

    %% Главное приложение
    class ToDoApp {
        -todo_list: ToDoList
        -current_user_id: int
        -current_username: str
        +setupUi(self)
        +show_login_dialog(): bool
        +setup_ui()
        +load_tasks()
        +on_item_double_clicked(item)
        +open_add_dialog()
        +closeEvent(event)
    }

    %% UI Классы (сгенерированные из .ui файлов)
    class Ui_MainWindow {
        <<interface>>
        +setupUi(self)
    }

    class Ui_Dialog {
        <<interface>>
        +setupUi(self)
    }

    class Ui_ChangeDialog {
        <<interface>>
        +setupUi(self)
    }

    class Ui_LoginDialog {
        <<interface>>
        +setupUi(self)
    }

    class Ui_TaskDetailsDialog {
        <<interface>>
        +setupUi(self)
    }

    %% PyQt5 базовые классы
    class QMainWindow {
        <<PyQt5>>
    }

    class QDialog {
        <<PyQt5>>
    }

    %% Отношения наследования
    ToDoApp --|> QMainWindow
    ToDoApp --|> Ui_MainWindow
    
    AddTaskDialog --|> QDialog
    AddTaskDialog --|> Ui_Dialog
    
    ChangeTaskDialog --|> QDialog
    ChangeTaskDialog --|> Ui_ChangeDialog
    
    LoginDialog --|> QDialog
    LoginDialog --|> Ui_LoginDialog
    
    TaskDetailsDialog --|> QDialog
    TaskDetailsDialog --|> Ui_TaskDetailsDialog

    %% Отношения композиции и агрегации
    ToDoApp *-- ToDoList : содержит
    ToDoList o-- Task : использует
    TaskDetailsDialog o-- ToDoList : использует
    ToDoApp ..> LoginDialog : создает
    ToDoApp ..> AddTaskDialog : создает
    ToDoApp ..> TaskDetailsDialog : создает
    TaskDetailsDialog ..> ChangeTaskDialog : создает

    %% База данных (концептуально)
    class Database {
        <<SQLite>>
        +users table
        +tasks table
    }
    
    ToDoList --> Database : подключается к

    %% Заметки к диаграмме
    note for ToDoList "Управляет базой данных\nи бизнес-логикой"
    note for ToDoApp "Главное окно приложения\nкоординирует все диалоги"
    note for Task "Модель данных\nдля задачи"
```

## Описание архитектуры:

### 1. **Модель данных (Data Model)**
- `Task`: Простая модель данных для задачи

### 2. **Слой данных (Data Layer)**
- `ToDoList`: Управляет всеми операциями с базой данных SQLite
- Обеспечивает аутентификацию пользователей
- Выполняет CRUD операции для задач

### 3. **Слой представления (Presentation Layer)**
- `ToDoApp`: Главное окно приложения
- `LoginDialog`: Диалог входа/регистрации
- `AddTaskDialog`: Диалог добавления новой задачи
- `ChangeTaskDialog`: Диалог редактирования задачи
- `TaskDetailsDialog`: Диалог просмотра деталей задачи

### 4. **UI Интерфейсы**
- Сгенерированные из QtDesigner .ui файлов
- Определяют внешний вид интерфейса

### 5. **Основные паттерны проектирования:**
- **MVC (Model-View-Controller)**: Разделение данных, представления и логики
- **Singleton**: ToDoList как единый менеджер базы данных
- **Factory**: Создание различных диалогов по требованию
- **Observer**: PyQt signals/slots для обработки событий
