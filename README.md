# Многопользовательское приложение "Список задач"

Десктопное приложение для управления задачами с системой аутентификации пользователей. Разработано на PyQt5 с базой данных SQLite.

## Архитектура системы

![UML Диаграмма классов](uml_2.png)

## Технологии

- **Python 3.7+** - язык программирования
- **PyQt5** - графический интерфейс
- **SQLite** - база данных
- **Qt Designer** - инструмент создания UI

## Функциональность

- **Аутентификация пользователей**: регистрация и вход с хешированием паролей
- **Управление задачами**: создание, редактирование, удаление задач
- **Система приоритетов**: 5 уровней приоритета (1-наивысший, 5-низший)
- **Подробный просмотр**: детальная информация по задаче
- **Изоляция пользователей**: каждый пользователь видит только свои задачи
- **Постоянство данных**: сохранение в SQLite

## Использование

1. **Регистрация/Вход**: создание аккаунта или вход в существующий
2. **Добавление задачи**: кнопка "Добавить задачу", заполнение формы
3. **Просмотр задач**: отображение всех задач пользователя в главном окне
4. **Редактирование**: двойной клик на задачу для просмотра деталей и редактирования
5. **Удаление**: кнопка удаления в окне деталей задачи

## Структура проекта

```
├── main.py                     # Основной файл приложения
├── dialog.ui                   # UI файл диалога добавления задачи
├── change_dialog.ui            # UI файл диалога редактирования
├── login_dialog.ui             # UI файл диалога входа
├── task_details_dialog.ui      # UI файл диалога деталей задачи
├── mainwindow.ui               # UI файл главного окна
├── ui_*.py                     # Сгенерированные Python файлы UI
├── todo_list.db               # База данных SQLite
├── requirements.txt           # Зависимости проекта
├── UML_Diagram.md            # UML диаграмма в Mermaid формате
└── UML.png                   # UML диаграмма классов
```

### База данных

**Таблица users:**
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password_hash (TEXT)
- created_at (INTEGER)

**Таблица tasks:**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY)
- title (TEXT)
- description (TEXT)
- priority (INTEGER)
- timestamp (INTEGER)

## Разработка

### Генерация UI файлов

При изменении .ui файлов необходимо регенерировать Python файлы:

```bash
pyuic5 -x mainwindow.ui -o ui_mainwindow_new.py
pyuic5 -x dialog.ui -o ui_dialog.py
pyuic5 -x change_dialog.ui -o ui_change_dialog.py
pyuic5 -x login_dialog.ui -o ui_login_dialog.py
pyuic5 -x task_details_dialog.ui -o ui_task_details_dialog.py
```

## Зависимости

Основные библиотеки проекта:
- PyQt5==5.15.11

Полный список в requirements.txt

## Future Enhancements

- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Data export/import functionality
- [ ] Dark theme support
- [ ] Task search and filtering
- [ ] Backup and restore features
