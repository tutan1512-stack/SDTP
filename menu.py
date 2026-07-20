# Функции интерфейса,  CRUD
import sdtp_db.model as bd
import crud as crud
import utils as utils
from typing import TypeVar
from datetime import datetime, date
from sqlalchemy import (
                        create_engine,
                        func,
                        select
 )

MODELS = {
    1: ("Типы свай", bd.TypePile),
    2: ("Испытуемые сваи", bd.TestedPile),
    3: ("Динамические испытания", bd.DynamicTested),
    4: ("Забивка", bd.DrivingLog),
    5: ("Добивка", bd.RedrivingLog),
    6: ("Абсолютные отметки", bd.AbsolutMark),
    7: ("Производители", bd.Producer),
    8: ("Категории производителей", bd.CategoryProducer),
    9: ("Транспорт", bd.Transport),
    10: ("Категории транспорта", bd.CategoryTransport),
    11: ("Молоты", bd.Hammer),
    12: ("Объекты", bd.BuildObject),
    13: ("Грунты", bd.Solid),
    14: ("Сотрудники", bd.Employee)
}

def database_menu():
    utils.clear()
    while True:
        utils.title("Просмотр базы данных")
        for key, value in MODELS.items():
            print(f"{key}.{value[0]}")
        print("\n[0] Назад")
        try:
            c = int(input("\n[>] Введите номер категории: "))
        except:
            continue
        if c==0:
            return
        if c in MODELS:
            utils.clear()

            utils.show_table(MODELS[c][1])

def delete_menu():
    while True:
        utils.title("Удаление записи")
        for key, value in MODELS.items(): # выводим из модели парключи
            print(f"{key}. {value[0]}")
        print("\n[0] Назад")
        try:
            c = int(input("\n[>] Выберите категорию: "))
        except:
            continue
        if c==0:
            return
        if c in MODELS:
            utils.delete_record(MODELS[c][1])

def main():
    while True:
        utils.title("СДИС")
        print("[1] Просмотр базы данных.")
        print("[2] Добавление записи.")
        print("[3] Удаление записи.")
        print("[0] Выход.")
        ans = input("\n[>] Введите номер действия: ")
        if ans == "1":
            database_menu()

        elif ans =="2":
            crud.add_menu()

        elif ans =="3":
            delete_menu()
            utils.pause()

        elif ans =="0":
            break

if __name__ == "__main__":
    main()

