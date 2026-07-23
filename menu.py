# Функции интерфейса,  CRUD
import crud as crud
import utils as utils
import traceback

def main():
    while True:
        utils.title("СДИС")
        print("[1] Просмотр базы данных.")
        print("[2] Добавление записи.")
        print("[3] Удаление записи.")
        print("\n[0] Выход.")
        ans = input("\n[>] Введите номер действия: ")
        if ans == "1":
            crud.database_menu()

        elif ans =="2":
            crud.add_menu()

        elif ans =="3":
            crud.delete_menu()
            utils.pause()

        elif ans =="0":
            break

if __name__ == "__main__":
    try:
        main()
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)

        print("[!] Произошла ошибка. Подробности записаны в error.log")
        input("[>] Нажмите Enter...")

