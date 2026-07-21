@echo off
chcp 65001 > nul
echo === Начало сборки приложения ===

REM 1. Проверяем, существует ли папка виртуального окружения. Если нет — создаем.
if not exist .venv (
    echo [1/4] Создание виртуального окружения .venv...
    python -m venv .venv
) else (
    echo [1/4] Виртуальное окружение .venv уже существует.
)

REM 2. Активируем виртуальное окружение и устанавливаем зависимости
echo [2/4] Активация окружения и установка зависимостей из requirements.txt...
call .\.venv\Scripts\activate.bat && pip install -r .\requirements.txt

REM 3. Запуск сборки через PyInstaller
echo [3/4] Запуск сборки приложения (pyinstaller)...
call .\.venv\Scripts\activate.bat && pyinstaller --onefile ./menu.py

REM 4. Финал
echo [4/4] Сборка успешно завершена! Ищите файл menu.exe в папке dist.
pause