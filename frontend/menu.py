# Функции интерфейса,  CRUD
from backend import utils as utils, crud as crud
from frontend import menus as menus
import traceback


if __name__ == "__main__":
    try:
        menus.menu()
    except Exception:
        with open("../error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)

        print("[!] Произошла ошибка. Подробности записаны в error.log")
        input("[>] Нажмите Enter...")

