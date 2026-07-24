# файл с универсальными функциями меню
import model as bd
import os, sys
from sqlalchemy import  select

def choose(model, title, display=None):
    session = bd.Session()
    try:
        data =session.scalars(select(model)).all()
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

def show_table( entity):
    model = entity['model']
    title(f"Просмотр: ({model.__tablename__})")
    session = bd.Session()
    try:
        data = session.query(model).order_by(model.id).all() # передаем очередь словарей из модели
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

def delete_record(kwargs):
    choice = choice_menu("Удаление записи", kwargs)
    session = bd.Session()
    try:
        if choice is None:
            print("\n[=] Запись не найдена\n")
            pause()
            return
        answer =  input("[>] Вы точно хотите удалить запись? (y/n)^ :")
        if answer.lower()=="y":
            session.delete(choice)
            session.commit(choice)
            print("\n[+] Запись удалена\n")
            pause()
    finally:
        session.close()

def add_record(kwargs):
    choice = choice_menu("Добавление записи", kwargs)

    if choice is None:
        return

    kwargs[choice]["add"]()

# функция приема и вывода выбора записи
def choice_menu(text, kwargs):
    while True:
        title(text)
        for key, item in kwargs.items():
            print(f"[{key}]{item['title']}")
        print("\n[0] Назад")
        try:
            ans = int(input("\n[>] Введите номер категории: "))
        except ValueError:
            continue
        if ans== 0:
            break
        if ans in kwargs:
            return ans
        else:
            print("[!] Неизвестная команда.")
            pause()


def search_menu(entity):
    model = entity["model"]
    session = bd.Session()
    try:
        while True:
            title(f"Поиск: {entity['title']}")

            for key, (text, attr) in entity["search"].items():
                print(f"[{key}] {text}")

            print("\n[0] Назад")
            try:
                cmd = int(input("\n[>] Поле поиска: "))
            except ValueError:
                continue
            if cmd == 0:
                return
            if cmd not in entity["search"]:
                continue

            text, attr = entity["search"][cmd]
            value = input(f"\n[>] Введите '{text}': ")
            column = getattr(model, attr)

            result = session.scalars(
                select(model).where(column == value)
            ).all()

            if not result:
                print("\n[!] Записи не найдены.")
            else:
                print()
                for obj in result:
                    print(obj)
                    print("-" * 40)

            pause()

    finally:
        session.close()