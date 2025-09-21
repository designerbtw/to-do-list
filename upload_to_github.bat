@echo off
echo =====================================================
echo 🚀 СКРИПТ ЗАГРУЗКИ ПРОЕКТА TO-DO LIST НА GITHUB
echo =====================================================
echo.

echo 📋 Проверяем наличие Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git не установлен!
    echo.
    echo 📦 Установите Git:
    echo 1. Откройте https://git-scm.com/download/win
    echo 2. Скачайте и установите Git
    echo 3. Перезапустите эту программу
    pause
    exit
)

echo ✅ Git установлен!
echo.

echo 📝 Настройка Git (если не настроен)...
set /p name="Введите ваше имя для Git: "
set /p email="Введите ваш email для Git: "

git config --global user.name "%name%"
git config --global user.email "%email%"

echo.
echo 🌍 Создайте репозиторий на GitHub:
echo 1. Откройте https://github.com/new
echo 2. Название: to-do-list
echo 3. Поставьте галочку Private
echo 4. НЕ добавляйте README/gitignore
echo 5. Нажмите Create repository
echo.
set /p repo_url="Введите URL вашего репозитория (https://github.com/username/to-do-list.git): "

echo.
echo 🔄 Инициализация Git...
git init
git add .
git commit -m "🎉 Первый коммит: добавлен проект TO-DO List с GUI на PyQt5"
git branch -M main
git remote add origin %repo_url%

echo.
echo 🚀 Загрузка на GitHub...
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ✅ УСПЕХ! Проект загружен на GitHub!
    echo 🌟 Ваш приватный репозиторий готов!
) else (
    echo ❌ Ошибка загрузки. Проверьте:
    echo - Правильность URL репозитория
    echo - Интернет соединение
    echo - Авторизацию на GitHub
)

echo.
pause