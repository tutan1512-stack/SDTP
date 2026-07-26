@echo off
chcp 65001 > nul
title SDIS Build

echo ========================================
echo        Сборка проекта СДИС
echo ========================================
echo.

:: Переход в каталог, где лежит bat-файл
cd /d "%~dp0"

:: Проверяем наличие виртуального окружения
if not exist ".venv\Scripts\python.exe" (
    echo [!] Виртуальное окружение не найдено.
    pause
    exit /b 1
)

echo [1/5] Обновление PyInstaller...
call .venv\Scripts\python.exe -m pip install --upgrade pyinstaller

if errorlevel 1 (
    echo.
    echo [!] Ошибка установки PyInstaller.
    pause
    exit /b 1
)

echo.
echo [2/5] Очистка предыдущей сборки...

if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist

echo.
echo [3/5] Сборка приложения...

call .venv\Scripts\python.exe -m PyInstaller SDIS.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo          СБОРКА ЗАВЕРШИЛАСЬ С ОШИБКОЙ
    echo ========================================
    pause
    exit /b 1
)

echo.
echo [4/5] Проверка результата...

if not exist "dist\SDIS\SDIS.exe" (
    echo [!] Исполняемый файл не найден.
    pause
    exit /b 1
)

echo.
echo ========================================
echo      Сборка успешно завершена!
echo ========================================
echo.
echo Исполняемый файл:
echo.
echo     dist\SDIS\SDIS.exe
echo.

pause