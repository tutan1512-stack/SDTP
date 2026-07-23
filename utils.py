# файл с универсальными функциями меню

import model as bd
import os, sys

FOREIGN = {
    "type_p_id": bd.TypePile,
    "prd_id":  bd.Producer,
    "object_id":  bd.BuildObject,
    "employee_id":  bd.Employee,
    "transport_id":  bd.Transport,
    "hammer_id":  bd.Hammer,
    "tested_id":  bd.DynamicTested,
    "tested_pile_id":  bd.TestedPile,
}

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


def choose(model, title, display=None):
    session = bd.Session()
    try:
        data = session.query(model).all()
        # если нет данных выводим
        if not data:
            print("\n[=] Таблица пуста.")
            input()
            return None
        print()

        for obj in data:
            # если передается текст, выведем его
            if display is None:
                text = str(obj)
            # если передается функция, вызываем ее
            elif callable(display):
                text = display(obj)
            # иначе возвращаем атрибут из объекта
            else:
                text = getattr(obj, display)
            print(f"{obj.id}. {text}")

# ждет айди  от пользователя
        while True:
            try:
                index = int(input(f"\n{title}: "))
                obj = session.get(model, index)
                if obj:
                    return obj.id
                print("[!] Такой записи нет.")
            except ValueError:
                print("[!] Введите число.")
    finally:
        session.close()

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    # функция очищения экрана

def pause():
    input("\n[>] Нажмите Enter...")

def title(name):
    clear()
    print("="*40)
    print(name.center(40))
    print("="*40)

def show_table( model):
    title(f"Просмотр: ({model.__tablename__})")
    session = bd.Session()
    try:
        data = session.query(model).all() # передаем очередь словарей из модели
        if not data:
            print("\n[=] Таблица пуста. \n")
            pause()
            return
        for row in data:
            print(row)
            print("-"*40)
    finally:
        session.close()
    pause()

def delete_record(model):
    title(f"Удаление ({model.__tablename__})")
    session = bd.Session()
    try:
        index = int(input("[>] Введите ID записи: "))
        obj = session.get(model, index)# получаем модель с нашим айди
        if obj is None:
            print("\n[=] Запись не найдена\n")
            pause()
            return
        print(obj)
        answer =  input("[>] Вы точно хотите удалить запись? (y/n)^ :")
        if answer.lower()=="y":
            session.delete(obj)
            session.commit()
            print("\n[=] Запись удалена\n")
    finally:
        session.close()
