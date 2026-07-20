# файл с универсальными функциями меню

import sdtp_db.model as bd
import os
def choose(model, title, display=None):
    session = bd.Session()
    try:
        data = session.query(model).all()

        if not data:
            print("\n[=] Таблица пуста.")
            input()
            return None

        print()

        for obj in data:
            if display is None:
                text = str(obj)
            elif callable(display):
                text = display(obj)
            else:
                text = getattr(obj, display)

            print(f"{obj.id}. {text}")

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