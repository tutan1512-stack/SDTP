# Конфигуратор пути
import os, sys

def get_appdata_db_path(app_name="MyPythonApp", db_name="database.db"):
    if getattr(sys, 'frozen', False):
        # На Windows os.getenv('APPDATA') ведет в C:\Users\Имя\AppData\Roaming
        base_dir = os.getenv('APPDATA')
        # Создаем там персональную папку для нашей программы, если её ещё нет
        app_dir = os.path.join(base_dir, app_name)
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        return os.path.join(app_dir, db_name)
    else:
        # При разработке храним локально в папке проекта
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
